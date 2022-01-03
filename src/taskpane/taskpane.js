/* eslint-disable no-undef */
const RunPython = require("./run_python");

Office.onReady((info) => {
  if (info.host === Office.HostType.Word) {
    if (!Office.context.requirements.isSetSupported("WordApi", "1.3")) {
      console.log("Sorry. The tutorial add-in uses Word.js APIs that are not available in your version of Office.");
    }
    document.getElementById("sideload-msg").style.display = "none";
    document.getElementById("app-body").style.display = "flex";
    document.getElementById("insert-paragraph").onclick = readSelectedRange;
  }
});

function readSelectedRange() {
  Word.run(function (context) {
    var doc = context.document;
    // load entire text of document body
    var wholeDoc = doc.body;
    wholeDoc.load("text");
    // load text of selected range
    var selectedRange = doc.getSelection();
    selectedRange.load("text");
    return context
      .sync()
      .then(function () {
        if (selectedRange.text != "") {
          var text = RunPython.runPython(selectedRange.text);
        } else {
          // eslint-disable-next-line no-redeclare
          var text = RunPython.runPython(wholeDoc.text);
        }
        doc.body.insertParagraph(text, "End");
      })
      .then(context.sync);
  }).catch(function (error) {
    console.log("Error: " + error);
    if (error instanceof OfficeExtension.Error) {
      console.log("Debug info: " + JSON.stringify(error.debugInfo));
    }
  });
}
