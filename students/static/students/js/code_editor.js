document.addEventListener("DOMContentLoaded", function() {
    // Создаем редактор CodeMirror из элемента textarea
    var editor = CodeMirror.fromTextArea(document.getElementById("code-editor"), {
      lineNumbers: true,  // Показывать номера строк
      mode: "python",     // Режим подсветки синтаксиса Python
      theme: "default"
    });
  });

document.getElementById("code-editor").style.display = "block";