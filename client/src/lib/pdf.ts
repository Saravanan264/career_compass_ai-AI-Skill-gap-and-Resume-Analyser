import * as pdfjsLib from "pdfjs-dist/legacy/build/pdf";

// ✅ Worker MUST match version
(pdfjsLib as any).GlobalWorkerOptions.workerSrc =
  "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js";

function clamp(n: number, min: number, max: number) {
  return Math.max(min, Math.min(max, n));
}

export async function extractTextFromPdf(
  file: File,
  onProgress?: (p: number) => void
): Promise<string> {
  const buffer = await file.arrayBuffer();
  onProgress?.(20);

  const loadingTask = pdfjsLib.getDocument({ data: buffer });
  const pdf = await loadingTask.promise;

  const totalPages = pdf.numPages || 1;
  let fullText = "";

  for (let pageNum = 1; pageNum <= totalPages; pageNum++) {
    const page = await pdf.getPage(pageNum);
    const content = await page.getTextContent();

    const pageText = (content.items as any[])
      .map((item) => ("str" in item ? item.str : ""))
      .join(" ");

    fullText += pageText + "\n";

    const progress = clamp(
      20 + Math.round((pageNum / totalPages) * 70),
      20,
      90
    );
    onProgress?.(progress);
  }

  onProgress?.(100);
  return fullText.trim();
}
