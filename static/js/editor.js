$(document).on('click', '#btn-editor-bold', function() {
  $('#editor-text').replaceAtCaret('text','bold');
})


jQuery.fn.extend({
insertAtCaret: function(myValue){
  return this.each(function(i) {
    if (document.selection) {
      //For browsers like Internet Explorer
      this.focus();
      sel = document.selection.createRange();
      sel.text = myValue;
      this.focus();
    }
    else if (this.selectionStart || this.selectionStart == '0') {
      //For browsers like Firefox and Webkit based
      var startPos = this.selectionStart;
      var endPos = this.selectionEnd;
      var scrollTop = this.scrollTop;
      this.value = this.value.substring(0, startPos)+myValue+this.value.substring(endPos,this.value.length);
      this.focus();
      this.selectionStart = startPos + myValue.length;
      this.selectionEnd = startPos + myValue.length;
      this.scrollTop = scrollTop;
    } else {
      this.value += myValue;
      this.focus();
    }
  })
}
});

// FUNC FOR INSERT NEAR SELECTION
$.fn.extend({
replaceAtCaret: function(myValue,myType){
  return this.each(function(i) {
    switch (myType) {
      case 'link':
        var insertBefore = "[[";
        var insertAfter = "]]";
      break;
      case "cat":
        var insertBefore = "[[Catégorie:";
        var insertAfter = "]]";
      break;
	  case 'italic':
        var insertBefore = "''";
        var insertAfter = "''";
      break;
	  case 'bold':
        var insertBefore = "'''";
        var insertAfter = "'''";
      break;
	  case 'nowiki':
        var insertBefore = "<nowiki>";
        var insertAfter = "</nowiki>";
      break;
	  case 'linkEx':
        var insertBefore = "[http:// ";
        var insertAfter = " ]";
      break;
      default:
        var insertBefore = "[[";
        var insertAfter = "]]";
      break;
    }
    if (this.selectionStart || this.selectionStart == '0') {
      //For browsers like Firefox and Webkit based
      var startPos = this.selectionStart;
      var endPos = this.selectionEnd;
      var scrollTop = this.scrollTop;
      var selectedText = this.value.substring( startPos, endPos)
      this.value = this.value.substring(0, startPos)+ insertBefore +selectedText + insertAfter +this.value.substring(endPos,this.value.length);
      this.focus();
      this.selectionStart = startPos + myValue.length;
      this.selectionEnd = startPos + myValue.length;
      this.scrollTop = scrollTop;
    } else {
      this.value += myValue;
      this.focus();
    }
  })
}
});

