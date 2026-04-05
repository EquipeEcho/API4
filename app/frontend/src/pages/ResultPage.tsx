import { useNavigate } from "react-router-dom";
import { Button } from "../components/Button";
import { EmptyState } from "../components/EmptyState";
import { CheckCircleIcon, DownloadIcon, InfoCircleIcon } from "../components/Icons";
import { PreviewPanel } from "../components/PreviewPanel";
import { SectionTitle } from "../components/SectionTitle";
import { usePrototype } from "../providers/PrototypeProvider";

// Exibe o documento gerado e as acoes de download.
export function ResultPage() {
    const navigate = useNavigate();
    const { currentDocument } = usePrototype();

  const downloadDocumentAsset = async (type:any) => {
    try {
      const response = await fetch(`/api/download/${type.toLowerCase()}`);

      if (!response.ok) throw new Error("Erro no download");

      const blob = await response.blob();

      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");

      a.href = url;
      a.download = `memorial.${type.toLowerCase()}`;
      a.click();

      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error(err);
    }
  };

  // Volta para a tela anterior ou para a home.
  const handleBack = () => {
    if (window.history.length > 1) {
      navigate(-1);
      return;
    }

    navigate("/");
  };

  if (!currentDocument) {
    return (
      <main className="page">
        <div className="page__content page__content--narrow">
          <EmptyState
            tone="error"
            icon={<InfoCircleIcon />}
            title="Nenhum memorial disponível"
            description="Conclua um processamento ou abra um item do histórico para visualizar o resultado."
            actionLabel="Ir para Home"
            onAction={() => navigate("/")}
          />
        </div>
      </main>
    );
  }

  return (
    <main className="page">
      <div className="page__content page__content--result">
        <section className="result-hero" aria-labelledby="result-title">
          <div className="result-hero__icon" aria-hidden="true">
            <CheckCircleIcon />
          </div>
          <SectionTitle
            className="result-hero__heading"
            eyebrow="Resultado"
            titleId="result-title"
            title="Processamento concluído"
            description="Os dados foram analisados com sucesso e o memorial está pronto para exportação."
            align="center"
          />
        </section>

        <PreviewPanel document={currentDocument} />

        <div className="result-actions">
          <Button
            variant="primary"
            leadingIcon={<DownloadIcon />}
            onClick={() => downloadDocumentAsset("XLSX")}
          >
            Baixar XSLX
          </Button>
          <Button
            variant="success"
            leadingIcon={<DownloadIcon />}
            onClick={() => downloadDocumentAsset("PDF")}
          >
            Baixar PDF
          </Button>
          <Button variant="secondary" onClick={handleBack}>
            Voltar
          </Button>
        </div>
      </div>
    </main>
  );
}
