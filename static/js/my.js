// MESSAGES
var print_message = function(msg,tag,into) {
  var html = '<div id="msg-'+tag+'" class="alert alert-'+tag+'" style="display: block;"><p class="pull-right"><button class="close" onclick="$(this).parent().parent().hide(250)">×</button></p><div>'+msg+'</div></div>';
  $(into).prepend(html);
}

// SEARCH PAGE
$(document).on('keypress', '#page_q', function(e) {
    if (e.which == 13 && $(this).val().length ) {
    $.ajax({url:'/search_page', async:true,
        data:{q:$(this).val(), type:$('#search-type').val()},
        success: function(data, status, xhr) {
            $('#search-pages').html(data);
        },
    });
    }
});

// CHOOSE AN ACTION FOR SEARCHED PAGES
$(document).on('change', '#search-pages-action', function() {
    if ( $(this).val() == 'add' ) {
        $('#search-pages :selected').appendTo('#pages');
    } else if ( $(this).val() == 'delete' ) {
        $('#search-pages :selected').remove();
    } else if ( $(this).val() == 'delete-all' ) {
        $('#search-pages option').remove();
    } else if ( $(this).val() == 'select-all' ) {
        $('#search-pages option').prop('selected', true);
    }
    $(this).val('---');
});
// WHY DOESN'T WORK ??
$(document).on('dbclick', '#search-pages', function() {
    $('#search-pages').children(':selected').appendTo('#pages');
});

// CHOOSE A META-ACTION FOR PAGES
$(document).on('change', '#pages-meta-action', function() {
    if ( $(this).val() == 'delete' ) {
        $('#pages option:selected').remove();
    } else if ( $(this).val() == 'delete-all' ) {
        $('#pages option').remove();
    } else if ( $(this).val() == 'select-all' ) {
        $('#pages option').prop('selected', true);
    }
    $(this).val('---');
});

// CHOOSE ACTION FOR SELECTED PAGES
$(document).on('change', '#pages-action', function() {
    var action = $(this).val();
    $('[id*=div-action]').hide(250);
    $('#div-action-'+action).show(250);
});

// REMOVE SELECTED PAGES
$(document).on('click', '#btn-delete-pages', function() {
    $('#pages').children(':selected').remove();
});

/// ACTIONS FOR SELECTED PAGES
// CHECK IF CATEGORY EXISTS
$(document).on('click', '.btn-check-page', function() {
  var target = $(this).parent().parent();
  var pagename = $( '#'+$(this).attr('rel') ).val()
  if ( $(this).hasClass('btn-check-category') ) {
    pagename = 'Catégorie:'+pagename
  }
  if ( pagename.length ) {
    $.ajax({url:'/check_page', data:{page:pagename}, async:true,
      success: function(data, status, xhr) {
        $(target).append(data);
      },
    });
  }
});

// RENAME PAGES
$(document).on('click', '#btn-rename-pages', function() {
    if ( $('#rename-from').val().length ) {
      $.ajax({type:'POST', url:'/move_pages', async:true,
          data:{
              pages:$('#pages').val(), 
              from:$('#rename-from').val(),
              to:$('#rename-to').val(),
              redirect:$('#rename-redirect:checked').val() || '',
              csrfmiddlewaretoken:csrf
          },
          success: function(data, status, xhr) {
              //$('#pages').empty();
              //$('#category-to-add').val('');
              $('#div-action-rename-pages').append(data);
          },
      });
    }
});

// ADD CATEGORY TO PAGES
$(document).on('click', '#btn-add-category', function() {
    if ( $('#category-to-add').val().length ) {
      $.ajax({type:'POST', url:'/add_category', async:true,
          data:{pages:$('#pages').val(), category:'Catégorie:'+$('#category-to-add').val(), csrfmiddlewaretoken:csrf},
          success: function(data, status, xhr) {
              //$('#pages').empty();
              //$('#category-to-add').val('');
              $('#div-action-add-category').append(data);
          },
      });
    }
});

// REMOVE CATEGORY
$(document).on('click', '#btn-remove-category', function() {
    if ( $('#category-to-remove').val().length ) {
      $.ajax({type:'POST', url:'/remove_category', async:true,
          data:{
              pages:$('#pages').val(),
              category:'Catégorie:'+$('#category-to-remove').val(),
              csrfmiddlewaretoken:csrf
          },
          success: function(data, status, xhr) {
              $('#div-action-remove-category').append(data);
          },
      });
    }
});

// MOVE CATEGORY
$(document).on('click', '#btn-move-category', function() {
    if ( $('#category-move-to').val().length && $('#category-move-from').val().length) {
      $.ajax({type:'POST', url:'/add_category', async:true,
          data:{
              pages:$('#pages').val(), 
              from:'Catégorie:'+$('#category-move-from').val(),
              to:'Catégorie:'+$('#category-move-to').val(),
              csrfmiddlewaretoken:csrf
          },
          success: function(data, status, xhr) {
              $('#div-action-move-category').append(data);
          },
      });
    }
});

// ADD HYPERLINKS
$(document).on('click', '#btn-add-hyperlink', function() {
  if ( $('#link-to-add').val().length ) {
    $.ajax({type:'POST', url:'/add_internal_link', async:true,
      data:{
        pages:$('#pages').val(), 
        link:$('#link-to-add').val(),
        link_text:$('#link-text').val(),
        csrfmiddlewaretoken:csrf
      },
      success: function(data, status, xhr) {
        $('#div-action-add-hyperlink').append(data);
      },
    });
  }
});

// SUBSITUTION
$(document).on('click', '#btn-sub', function() {
  if ( $('#sub-from').val().length ) {
    $.ajax({type:'POST', url:'/sub', async:true,
      data:{
        pages:$('#pages').val(), 
        from:$('#sub-from').val(),
        to:$('#sub-to').val(),
        csrfmiddlewaretoken:csrf
      },
      success: function(data, status, xhr) {
        $('#div-action-sub').append(data);
      },
    });
  }
});


// INFINITE LOOP FOR ASYNC TASKS
if ( CELERY_IS_ACTIVE ) {
window.onload = function start() {
    get_finished_tasks();
}
      }
function get_finished_tasks() {
    window.setInterval(function () {
        $.ajax({type:'GET', url:'/get_finished_tasks', async:true,
          success: function(data, status, xhr) {
            $('#action-msg-box').append(data);
          },
        });
    }, 10000);
}

// SEARCH CONTRIBUTIONS
$(document).on('keypress', '#contrib_q', function(e) {
    if (e.which == 13 && $(this).val().length ) {
    $.ajax({url:'/search_contribution', async:true,
        data:{q:$(this).val()},
        success: function(data, status, xhr) {
            $('#contribs').html(data);
        },
    });
    }
});

// SEARCH PAGE FOR EDITOR 
$(document).on('keypress', '#editor_q', function(e) {
    if (e.which == 13 && $(this).val().length ) {
	var page = $(this).val()
    $.ajax({url:'/get_page_text', async:true,
        data:{q:page},
        success: function(data, status, xhr) {
            $('#editor-page').val(page);
            $('#editor-text').val(data);
			if (data == '') {
			  print_message('Page vide.','warning','#editor-messages')
			}
        },
    });
    }
});

// PUT PAGE FOR EDITOR 
$(document).on('click', '#btn-publish-editor', function() {
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
	}
  });
});

// GET REGISTERED USER FORM
$(document).on('click', '#btn-get-wikiuser', function() {
  $.ajax({type:'GET', url:'/get_user', async:true,
    data:{id:$('input[name="user-chosen"]:checked').val()},
    success: function(data, status, xhr) {
      $('#user-form').html(data);
	}
  });
});
//
// GET NOT REGISTERED USER FORM
$(document).on('click', '#btn-get-form-wikiuser', function() {
  $.ajax({type:'GET', url:'/get_user', async:true,
    success: function(data, status, xhr) {
      $('#user-form').html(data);
	}
  });
});

// ADD USER
$(document).on('click', '#btn-add-wikiuser', function() {
  $.ajax({type:'POST', url:'/add_user', async:true,
    data:{
	  nick:$('#id_nick').val(),
	  family:$('#id_family').val(),
	  language:$('#id_language').val(),
	  url:$('#id_url').val(),
	  comment:$('#id_comment').val(),
	  active:($('#id_active:checked').val() || 'off'),
      csrfmiddlewaretoken:csrf
	},
    success: function(data, status, xhr) {
      $('#user-form-messages').prepend(data);
	}
  });
});

// UPDATE USER
$(document).on('click', '#btn-update-wikiuser', function() {
  $.ajax({type:'POST', url:'/update_user', async:true,
    data:{
	  id:$('#id_id').val(),
	  nick:$('#id_nick').val(),
	  family:$('#id_family').val(),
	  language:$('#id_language').val(),
	  url:$('#id_url').val(),
	  comment:$('#id_comment').val(),
	  active:($('#id_active:checked').val() || 'off'),
      csrfmiddlewaretoken:csrf
	},
    success: function(data, status, xhr) {
      $('#user-form-messages').prepend(data);
	}
  });
});

// DELETE USER
$(document).on('click', '#btn-delete-wikiuser', function() {
  $.ajax({type:'POST', url:'/delete_user', async:true,
    data:{
	  id:$('#id_id').val(),
      csrfmiddlewaretoken:csrf
	},
    success: function(data, status, xhr) {
      $('#user-list').html(data);
      $('#btn-get-form-wikiuser').click();
      print_message('Utilisateur supprimé.','error','#user-messages');
	}
  });
});

// CHOOSE USER
$(document).on('click', '#btn-choose-wikiuser', function() {
  $.ajax({type:'POST', url:'/set_active_user', async:true,
    data:{
      id:$('#user-chosen:checked').val(),
	  active:'on',
      csrfmiddlewaretoken:csrf
	},
    success: function(data, status, xhr) {
      $('#user-messages').prepend(data);
      setTimeout(window.location.reload, 3000);
	}
  });
});
