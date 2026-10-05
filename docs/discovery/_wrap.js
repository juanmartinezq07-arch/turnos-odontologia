// Wrapper: convierte el fragmento HTML de marked en un documento imprimible.
const fs = require('fs');
const path = require('path');

const dir = path.join(__dirname);
const body = fs.readFileSync(path.join(dir, '_informe.body.html'), 'utf8');

const css = `
@page { size: A4; margin: 18mm 14mm 16mm 14mm; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body {
  font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
  font-size: 10pt; line-height: 1.5; color: #1a1a1a; margin: 0;
}
h1 { font-size: 20pt; color: #0b3d5c; border-bottom: 2.5px solid #0b3d5c;
     padding-bottom: 6px; margin: 0 0 14px; page-break-after: avoid; }
h2 { font-size: 14pt; color: #0b3d5c; border-bottom: 1px solid #b8ccd8;
     padding-bottom: 3px; margin: 20px 0 10px; page-break-after: avoid; }
h3 { font-size: 11.5pt; color: #14506f; margin: 14px 0 7px; page-break-after: avoid; }
h4 { font-size: 10.5pt; color: #1c5c7d; margin: 12px 0 6px; page-break-after: avoid; }
p { margin: 0 0 8px; text-align: justify; }
ul, ol { margin: 0 0 9px; padding-left: 20px; }
li { margin-bottom: 3px; }
strong { color: #000; }
em { color: #333; }
code { font-family: "Consolas", "Courier New", monospace; font-size: 8.6pt;
       background: #f2f5f7; padding: 1px 4px; border-radius: 3px; color: #0b3d5c; }
pre { background: #f6f8f9; border-left: 3px solid #b8ccd8; padding: 8px 10px;
      overflow-x: auto; page-break-inside: avoid; }
pre code { background: none; padding: 0; }
blockquote { border-left: 3px solid #0b3d5c; background: #f4f8fa;
             margin: 10px 0; padding: 8px 12px; page-break-inside: avoid; }
blockquote p { margin: 0 0 6px; }
hr { border: none; border-top: 1px solid #d5dee4; margin: 16px 0; }
table { border-collapse: collapse; width: 100%; margin: 10px 0 14px;
        font-size: 7.6pt; line-height: 1.32; page-break-inside: avoid; }
th { background: #0b3d5c; color: #fff; text-align: left; font-weight: 600;
     padding: 4px 5px; border: 1px solid #0b3d5c; vertical-align: bottom; }
td { border: 1px solid #ccd8de; padding: 4px 5px; vertical-align: top;
     word-break: break-word; overflow-wrap: anywhere; }
tbody tr:nth-child(even) td { background: #f6f9fa; }
table strong { font-weight: 700; }
thead { display: table-header-group; }
a { color: #14506f; text-decoration: none; }
`;

const html = `<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>Informe de Discovery competitivo — Gestion odontologica</title>
<style>${css}</style>
</head>
<body>
${body}
</body>
</html>
`;

fs.writeFileSync(path.join(dir, '_informe.print.html'), html, 'utf8');
console.log('OK _informe.print.html');
