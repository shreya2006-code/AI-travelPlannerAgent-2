import { toPng } from "html-to-image";
import jsPDF from "jspdf";

export async function exportItineraryPDF(elementId: string) {
  const input = document.getElementById(elementId);

  const exportBtn = document.getElementById("export-btn");

  if (exportBtn) {
    exportBtn.style.display = "none";
  }

  if (!input) return;

  const dataUrl = await toPng(input, {
    cacheBust: true,
    pixelRatio: 2,
    backgroundColor: "#09090b",
  });

  const pdf = new jsPDF("p", "mm", "a4");

  const imgProps = pdf.getImageProperties(dataUrl);

  const pdfWidth = pdf.internal.pageSize.getWidth();

  const pdfHeight =
    (imgProps.height * pdfWidth) / imgProps.width;

  pdf.addImage(
    dataUrl,
    "PNG",
    0,
    0,
    pdfWidth,
    pdfHeight
  );

  pdf.save("AI-Travel-Itinerary.pdf");

  if (exportBtn) {
    exportBtn.style.display = "";
  }
}