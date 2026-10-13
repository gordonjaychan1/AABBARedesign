// Converts HTML files (from `textutil -convert html some.docx`) to paginated US Letter PDFs with macOS AppKit.
// Usage: osascript -l JavaScript tools/html_to_pdf.js <in.html> <out.pdf> [<in.html> <out.pdf> ...]
ObjC.import('AppKit');
function run(argv) {
  $.NSApplication.sharedApplication;
  const out = [];
  for (let i = 0; i + 1 < argv.length; i += 2) {
    const src = $.NSURL.fileURLWithPath(argv[i]), dst = $.NSURL.fileURLWithPath(argv[i + 1]);
    const opts = $.NSDictionary.dictionaryWithObjectForKey($.NSHTMLTextDocumentType, $.NSDocumentTypeDocumentOption);
    const err = Ref();
    const text = $.NSAttributedString.alloc.initWithURLOptionsDocumentAttributesError(src, opts, null, err);
    if (text.isNil()) { out.push('FAILED read ' + argv[i]); continue; }

    const info = $.NSPrintInfo.alloc.init;
    info.paperSize = $.NSMakeSize(612, 792);           // US Letter
    info.topMargin = 54; info.bottomMargin = 54; info.leftMargin = 64; info.rightMargin = 64;
    info.horizontalPagination = $.NSPrintingPaginationModeFit;
    info.verticalPagination = $.NSPrintingPaginationModeAutomatic;
    info.verticallyCentered = false; info.horizontallyCentered = false;
    info.jobDisposition = $.NSPrintSaveJob;
    info.dictionary.setObjectForKey(dst, $.NSPrintJobSavingURL);

    const width = 612 - 64 - 64;
    const view = $.NSTextView.alloc.initWithFrame($.NSMakeRect(0, 0, width, 10));
    view.textContainerInset = $.NSMakeSize(0, 0);
    view.textContainer.lineFragmentPadding = 0;
    view.verticallyResizable = true;
    view.textStorage.setAttributedString(text);
    view.layoutManager.ensureLayoutForTextContainer(view.textContainer);
    view.sizeToFit;

    const op = $.NSPrintOperation.printOperationWithViewPrintInfo(view, info);
    op.showsPrintPanel = false; op.showsProgressPanel = false;
    out.push((op.runOperation ? 'ok ' : 'FAILED write ') + argv[i + 1]);
  }
  return out.join('\n');
}
