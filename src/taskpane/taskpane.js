/* eslint-disable no-redeclare */
/* eslint-disable no-undef */
/*
 * Copyright (c) Microsoft Corporation. All rights reserved. Licensed under the MIT license.
 * See LICENSE in the project root for license information.
 */

/* global document, Office, Word */

Office.onReady((info) => {
  // Determine if the user's version of Office supports all the Office.js APIs that are used in the tutorial.
  if (!Office.context.requirements.isSetSupported("WordApi", "1.3")) {
    console.log("Sorry. The tutorial add-in uses Word.js APIs that are not available in your version of Office.");
  }

  // Assign event handlers and other initialization logic.
  document.getElementById("test").onclick = test;
  document.getElementById("read-selected-range").onclick = readSelectedRange;
  if (info.host === Office.HostType.Word) {
    document.getElementById("sideload-msg").style.display = "none";
    document.getElementById("app-body").style.display = "flex";
  }
});

function test() {
  var content;
  var fs = require("fs");
  fs.readFile("output.txt", function read(err, data) {
    if (err) {
      throw err;
    }
    content = data;
  });
  Word.run(function (context) {
    var docBody = context.document.body;
    docBody.insertParagraph(content, "End");
    return context.sync();
  }).catch(function (error) {
    console.log("Error: " + error);
    if (error instanceof OfficeExtension.Error) {
      console.log("Debug info: " + JSON.stringify(error.debugInfo));
    }
  });
}

function readSelectedRange() {
  var content;
  var fs = require("fs");
  fs.readFile("output.txt", function read(err, data) {
    if (err) {
      throw err;
    }
    content = data;
  });
  Word.run(function (context) {
    var docBody = context.document.body;
    docBody.insertParagraph("add something", "End");
    return context.sync();
  }).catch(function (error) {
    console.log("Error: " + error);
    if (error instanceof OfficeExtension.Error) {
      console.log("Debug info: " + JSON.stringify(error.debugInfo));
    }
  });
}
