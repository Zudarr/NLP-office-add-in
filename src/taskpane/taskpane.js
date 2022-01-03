/* eslint-disable no-redeclare */
/* eslint-disable no-undef */
Office.onReady((info) => {
  if (info.host === Office.HostType.Word) {
    if (!Office.context.requirements.isSetSupported("WordApi", "1.3")) {
      console.log("Sorry. The tutorial add-in uses Word.js APIs that are not available in your version of Office.");
    }
    document.getElementById("sideload-msg").style.display = "none";
    document.getElementById("app-body").style.display = "flex";
    document.getElementById("read-selected-range").onclick = readSelectedRange;
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
          var text = selectedRange.text;
        } else {
          var text = wholeDoc.text;
        }
        var statisticResult = "";
        var child_process = require("child_process").spawn;
        var process = child_process("python", ["../PythonCode/NLP.py", text]);
        process.stdout.on("data", (data) => {
          statisticResult = data.toString();
        });
        doc.body.insertParagraph(statisticResult, "End");
        //doc.body.insertParagraph(text, "End");
      })
      .then(context.sync);
  }).catch(function (error) {
    console.log("Error: " + error);
    if (error instanceof OfficeExtension.Error) {
      console.log("Debug info: " + JSON.stringify(error.debugInfo));
    }
  });
}
