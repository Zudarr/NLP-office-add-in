import axios from "axios"

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
      .then(async function () {
        if (selectedRange.text != "") {
          var text = selectedRange.text;
        } else {
          var text = wholeDoc.text;
        }
        const data = await getData(text);
        Object.keys(data).forEach(key => {
          doc.body.insertParagraph(key.toString() + ":" + data[key].toString(), "End");
        });
        
      })
      .then(context.sync);
  }).catch(function (error) {
    console.log("Error: " + error);
    if (error instanceof OfficeExtension.Error) {
      console.log("Debug info: " + JSON.stringify(error.debugInfo));
    }
  });
}

const getData = async (content) => {
  const form = new FormData();
  form.append("text", content);
  const data = await axios
    .post("http://127.0.0.1:5000/", form, {
      mode: "no-cors",
      headers: {
        "Content-Type": "multipart/form-data",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "*",
        "Access-Control-Allow-Credentials": "true",
      },
    })
    .then((res) => res.data);
  return data;
};