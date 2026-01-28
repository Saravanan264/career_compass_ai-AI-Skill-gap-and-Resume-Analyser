import * as pdfjsLib from "pdfjs-dist";

// Use the worker from a CDN to avoid bundler worker config.
// This is a demo-friendly approach for the prototype.
(pdfjsLib as any).GlobalWorkerOptions.workerSrc =
  "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/4.10.38/pdf.worker.min.mjs";

function clamp(n: number, min: number, max: number) {
  return Math.max(min, Math.min(max, n));
}

export async function extractTextFromPdf(
  file: File,
  onProgress?: (p: number) => void,
): Promise<string> {
  const buf = await file.arrayBuffer();
  onProgress?.(22);

  const pdf = await pdfjsLib.getDocument({ data: buf }).promise;
  const total = pdf.numPages || 1;

  let full = "";
  for (let i = 1; i <= total; i++) {
    const page = await pdf.getPage(i);
    const content = await page.getTextContent();
    const text = (content.items as any[])
      .map((it) => ("str" in it ? it.str : ""))
      .join(" ");

    full += text + "\n";
    const p = clamp(22 + Math.round((i / total) * 58), 22, 82);
    onProgress?.(p);
  }

  return full;
}
