import {
  PropsWithChildren,
  createContext,
  useContext,
  useEffect,
  useRef,
  useState,
} from "react";
import {
  buildGeneratedDocumentFromUploads,
  buildHistoryDocumentFromGenerated,
  getFileKindFromName,
  mockHistoryDocuments,
} from "../data/mockData";
import {
  AddFilesResult,
  GeneratedDocument,
  HistoryDocument,
  ToastState,
  ToastTone,
  UploadDocument,
} from "../types/documents";

type PrototypeContextValue = {
  uploadedFiles: UploadDocument[];
  historyDocuments: HistoryDocument[];
  currentDocument: GeneratedDocument | null;
  toast: ToastState | null;
  addUploadedFiles: (fileList: FileList | File[]) => AddFilesResult;
  removeUploadedFile: (documentId: string) => void;
  clearUploadedFiles: () => void;
  completeProcessing: () => GeneratedDocument | null;
  openHistoryPreview: (documentId: string) => void;
  removeHistoryDocument: (documentId: string) => void;
  downloadHistoryBundle: () => void;
  simulatePreviewAction: (fileName: string) => void;
  downloadDocumentAsset: (label: string) => void;
  showToast: (message: string, tone?: ToastTone) => void;
};

const PrototypeContext = createContext<PrototypeContextValue | null>(null);

function buildUploadDocument(file: File): UploadDocument | null {
  const kind = getFileKindFromName(file.name);

  if (!kind) {
    return null;
  }

  return {
    id: `${file.name}-${file.size}-${file.lastModified}`,
    name: file.name,
    kind,
  };
}

export function PrototypeProvider({ children }: PropsWithChildren) {
  const [uploadedFiles, setUploadedFiles] = useState<UploadDocument[]>([]);
  const uploadedFilesRef = useRef<UploadDocument[]>([]);
  const [historyDocuments, setHistoryDocuments] =
    useState<HistoryDocument[]>(mockHistoryDocuments);
  const [currentDocument, setCurrentDocument] = useState<GeneratedDocument | null>(
    null
  );
  const [toast, setToast] = useState<ToastState | null>(null);

  useEffect(() => {
    if (!toast) {
      return;
    }

    const timeoutId = window.setTimeout(() => {
      setToast(null);
    }, 2600);

    return () => {
      window.clearTimeout(timeoutId);
    };
  }, [toast]);

  const showToast = (message: string, tone: ToastTone = "info") => {
    setToast({
      id: Date.now(),
      tone,
      message,
    });
  };

  const syncUploadedFiles = (nextFiles: UploadDocument[]) => {
    uploadedFilesRef.current = nextFiles;
    setUploadedFiles(nextFiles);
  };

  const addUploadedFiles = (fileList: FileList | File[]): AddFilesResult => {
    const incomingFiles = Array.from(fileList);
    const parsedFiles = incomingFiles.map(buildUploadDocument);
    const currentFiles = uploadedFilesRef.current;
    const nextFiles = [...currentFiles];
    const knownIds = new Set(currentFiles.map((file) => file.id));
    let duplicateCount = 0;
    let invalidCount = 0;
    let addedCount = 0;

    parsedFiles.forEach((file) => {
      if (!file) {
        invalidCount += 1;
        return;
      }

      if (knownIds.has(file.id)) {
        duplicateCount += 1;
        return;
      }

      knownIds.add(file.id);
      nextFiles.push(file);
      addedCount += 1;
    });

    if (addedCount > 0) {
      syncUploadedFiles(nextFiles);
    }

    return { addedCount, duplicateCount, invalidCount };
  };

  const removeUploadedFile = (documentId: string) => {
    syncUploadedFiles(
      uploadedFilesRef.current.filter((document) => document.id !== documentId)
    );
  };

  const clearUploadedFiles = () => {
    syncUploadedFiles([]);
  };

  const completeProcessing = () => {
    const filesToProcess = uploadedFilesRef.current;

    if (filesToProcess.length === 0) {
      return null;
    }

    const generatedDocument = buildGeneratedDocumentFromUploads(filesToProcess);
    const historyDocument = buildHistoryDocumentFromGenerated(generatedDocument);

    setCurrentDocument(generatedDocument);
    setHistoryDocuments((currentHistory) => [historyDocument, ...currentHistory]);
    syncUploadedFiles([]);
    showToast("Processamento concluído com sucesso.", "success");

    return generatedDocument;
  };

  const openHistoryPreview = (documentId: string) => {
    const historyDocument = historyDocuments.find(
      (document) => document.id === documentId
    );

    if (!historyDocument) {
      showToast("Documento não encontrado.", "error");
      return;
    }

    setCurrentDocument(historyDocument.document);
  };

  const removeHistoryDocument = (documentId: string) => {
    setHistoryDocuments((currentHistory) =>
      currentHistory.filter((document) => document.id !== documentId)
    );
    showToast("Documento removido do histórico.", "info");
  };

  const downloadHistoryBundle = () => {
    if (historyDocuments.length === 0) {
      showToast("Não há documentos no histórico para download.", "error");
      return;
    }

    showToast("Pacote do histórico pronto para download.", "success");
  };

  const simulatePreviewAction = (fileName: string) => {
    showToast(`Pré-visualização simulada: ${fileName}.`, "info");
  };

  const downloadDocumentAsset = (label: string) => {
    const assetLabel = label.includes(".") ? "arquivo" : label;
    showToast(`Download de ${assetLabel} iniciado.`, "success");
  };

  return (
    <PrototypeContext.Provider
      value={{
        uploadedFiles,
        historyDocuments,
        currentDocument,
        toast,
        addUploadedFiles,
        removeUploadedFile,
        clearUploadedFiles,
        completeProcessing,
        openHistoryPreview,
        removeHistoryDocument,
        downloadHistoryBundle,
        simulatePreviewAction,
        downloadDocumentAsset,
        showToast,
      }}
    >
      {children}
    </PrototypeContext.Provider>
  );
}

export function usePrototype() {
  const context = useContext(PrototypeContext);

  if (!context) {
    throw new Error("usePrototype must be used within PrototypeProvider.");
  }

  return context;
}
