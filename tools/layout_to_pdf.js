// Lays out a document described by tools/docx_to_pdf.py (JSON) and saves it as a US Letter PDF using
// macOS AppKit's text system, so list numbers, hanging indents, tabs and fonts match the Word file.
// Usage: osascript -l JavaScript tools/layout_to_pdf.js <layout.json> <out.pdf>
ObjC.import('AppKit');
ObjC.import('Foundation');
function run(argv) {
  $.NSApplication.sharedApplication;
  var doc = JSON.parse(ObjC.unwrap($.NSString.stringWithContentsOfFileEncodingError(argv[0], $.NSUTF8StringEncoding, null)));
  // Text is written straight into the view's storage: this JXA bridge doesn't expose NSAttributedString's initializers.
  var view = $.NSTextView.alloc.initWithFrame($.NSMakeRect(0, 0, 612 - 144, 10));
  view.textContainerInset = $.NSMakeSize(0, 0);
  view.textContainer.lineFragmentPadding = 0;
  view.verticallyResizable = true;
  var ts = view.textStorage;
  var FONTS = { '': 'TimesNewRomanPSMT', b: 'TimesNewRomanPS-BoldMT', i: 'TimesNewRomanPS-ItalicMT', bi: 'TimesNewRomanPS-BoldItalicMT' };
  function font(bold, italic, size) {
    return $.NSFont.fontWithNameSize(FONTS[(bold ? 'b' : '') + (italic ? 'i' : '')], size) || $.NSFont.systemFontOfSize(size);
  }
  doc.paragraphs.forEach(function (p) {
    var ps = $.NSMutableParagraphStyle.alloc.init;
    // measured: through this bridge 1 centers and 2 right-aligns (the named constants are swapped)
    ps.alignment = p.align === 'center' ? 1 : p.align === 'right' ? 2 : 0;
    ps.headIndent = p.left;
    ps.firstLineHeadIndent = p.marker ? Math.max(0, p.left - p.hang) : p.left;
    ps.paragraphSpacing = 4;
    ps.defaultTabInterval = 36;
    // a list item's text starts at its indent, right after the number
    ps.tabStops = p.marker ? $([$.NSTextTab.alloc.initWithTextAlignmentLocationOptions($.NSTextAlignmentLeft, p.left, $.NSDictionary.dictionary)]) : $([]);
    function add(text, bold, italic, underline, size) {
      var attrs = $.NSMutableDictionary.dictionary;
      attrs.setObjectForKey(font(bold, italic, size), $.NSFontAttributeName);
      attrs.setObjectForKey(ps, $.NSParagraphStyleAttributeName);
      if (underline) attrs.setObjectForKey($(1), $.NSUnderlineStyleAttributeName);
      var start = ts.length;
      ts.mutableString.appendString($(text));
      ts.setAttributesRange(attrs, $.NSMakeRange(start, ts.length - start));
    }
    var size = (p.runs[0] && p.runs[0].size) || doc.size;
    if (p.marker) add(p.marker + '\t', false, false, false, size);
    p.runs.forEach(function (r) { add(r.text, r.b, r.i, r.u, r.size || doc.size); });
    add('\n', false, false, false, size);
  });

  var info = $.NSPrintInfo.alloc.init;
  info.paperSize = $.NSMakeSize(612, 792);
  info.topMargin = 54; info.bottomMargin = 54; info.leftMargin = 72; info.rightMargin = 72;
  info.horizontalPagination = $.NSPrintingPaginationModeFit;
  info.verticalPagination = $.NSPrintingPaginationModeAutomatic;
  info.verticallyCentered = false; info.horizontallyCentered = false;
  info.jobDisposition = $.NSPrintSaveJob;
  info.dictionary.setObjectForKey($.NSURL.fileURLWithPath(argv[1]), $.NSPrintJobSavingURL);
  view.layoutManager.ensureLayoutForTextContainer(view.textContainer);
  view.sizeToFit;

  var op = $.NSPrintOperation.printOperationWithViewPrintInfo(view, info);
  op.showsPrintPanel = false; op.showsProgressPanel = false;
  return (op.runOperation ? 'ok ' : 'FAILED ') + argv[1];
}
