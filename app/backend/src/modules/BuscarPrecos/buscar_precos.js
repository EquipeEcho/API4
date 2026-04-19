const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

// 🧠 Limpeza inteligente
function limparDescricao(desc) {
    if (!desc) return null;

    desc = desc.toLowerCase();

    if (desc.includes("line")) return "cabo elétrico";
    if (desc.includes("revestimento")) return "cimento";
    if (desc.includes("tubo")) return "tubo pvc";
    if (desc.includes("fio")) return "fio elétrico";

  
    return desc;
}

// 💰 Converter preço
function extrairNumero(preco) {
    if (!preco) return null;

    return parseFloat(
        preco
            .replace(/\./g, '')
            .replace(',', '.')
            .replace(/[^\d.]/g, '')
    );
}

async function executar() {

    const browser = await puppeteer.launch({
        headless: true, // ⚡ mais rápido
        args: ['--no-sandbox']
    });

    const page = await browser.newPage();
    await page.setUserAgent(
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36'
);

    // 📂 HTML
    const caminhoHTML = 'file://' + path.join(__dirname, '../ExtracaoDados/visualizacao.html');

    await page.goto(caminhoHTML);

    console.log("✔ HTML carregado");

    // 📊 Extrair dados
    const materiais = await page.evaluate(() => {
        const linhas = document.querySelectorAll('table tbody tr');

        let dados = [];

        linhas.forEach(linha => {
            const colunas = linha.querySelectorAll('td');

            dados.push({
                descricao: colunas[1]?.innerText.trim(),
                quantidade: parseFloat(colunas[3]?.innerText.trim())
            });
        });

        return dados;
    });

    console.log(`✔ ${materiais.length} itens encontrados`);

    let resultados = [];
    let cache = {}; // ⚡ evita buscas repetidas

    for (let item of materiais) {

        let query = limparDescricao(item.descricao);

        if (!query) continue;

        // ⚡ CACHE
        if (cache[query]) {
            console.log("⚡ Cache:", query);

            resultados.push({
                descricao: query,
                quantidade: item.quantidade,
                preco: cache[query],
                total: cache[query] * item.quantidade
            });

            continue;
        }

        console.log("🔎 Buscando:", query);

        try {
            await page.goto(`https://lista.mercadolivre.com.br/${encodeURIComponent(query)}`, {
                waitUntil: 'domcontentloaded'
            });

            // ⚡ espera inteligente
            await page.waitForSelector('span.andes-money-amount__fraction', { timeout: 5000 });

            const precoTexto = await page.evaluate(() => {
                const el = document.querySelector('span.andes-money-amount__fraction');
                return el ? el.innerText : null;
            });

            const precoNumero = extrairNumero(precoTexto);

            // salvar no cache
            if (precoNumero) {
                cache[query] = precoNumero;
            }

            resultados.push({
                descricao: query,
                quantidade: item.quantidade,
                preco: precoNumero,
                total: precoNumero ? precoNumero * item.quantidade : null
            });

        } catch (err) {
            console.log("❌ Erro em:", query);

            resultados.push({
                descricao: query,
                quantidade: item.quantidade,
                preco: null,
                total: null
            });
        }
    }

    // 💾 salvar resultado
    const caminhoSaida = path.join(__dirname, '../resultado/resultado_precos.json');

    // cria pasta automaticamente
    fs.mkdirSync(path.dirname(caminhoSaida), { recursive: true });

    fs.writeFileSync(caminhoSaida, JSON.stringify(resultados, null, 4));

    console.log("✅ Finalizado com sucesso!");

    await browser.close();
}

executar();