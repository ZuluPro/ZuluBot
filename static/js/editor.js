// GET PAGE
$(document).on('click', '#btn-search-editor', function() {
    if ( $('#editor_q').val().length ) {
      print_loading_gif('#editor-messages',50,50);
	  var page = $('#editor_q').val()
      $.ajax({url:'/get_page_text', async:true,
          data:{q:page},
          success: function(data, status, xhr) {
              $('#editor-page').val(page);
              $('#editor-text').val(data);
	  		if (data == '') {
	  		  print_message('Page vide.','warning','#editor-messages')
	  		}
          },
          complete: function(data, status, xhr) {
            remove_loading_gif('#editor-messages');
          },
      });
    }
});
// GET PAGE BY PRESS ENTER
$(document).on('keypress', '#editor_q', function(e) {
  if (e.which == 13) {
    $('#btn-search-editor').click();
  }
});

// PUT PAGE FOR EDITOR 
$(document).on('click', '#btn-publish-editor', function() {
  print_loading_gif('#editor-messages',50,50);
  $.ajax({type:'POST', url:'/put_page_text', async:true,
    data:{
	  page:$('#editor-page').val(),
      text:$('#editor-text').val(),
      comment:$('#editor-comment').val(),
      //minor:$('#editor-comment').val()
      csrfmiddlewaretoken:csrf
	},
    success: function(data, status, xhr) {
      $('#editor-messages').prepend(data);
	},
    complete: function(data, status, xhr) {
      remove_loading_gif('#editor-messages');
    },
  });
});

// CANCEL PAGE EDITION
$(document).on('click', '#btn-reinit-editor', function() {
  var page = $('#editor-page').val();
  $('#editor_q').val(page);
  $('#btn-search-editor').click();
});

// INSERT BOLD TAGS
$(document).on('click', '#btn-editor-bold', function() {
  $('#editor-text').replaceAtCaret('text','bold');
})

// INSERT AN EMPTY UNORDERED LIST
$(document).on('click', '#btn-editor-list', function() {
  $('#editor-text').insertAtCaret('*\n*\n');
})

// FUNC FOR INSERT AT SELECTION
$.fn.extend({
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

