// SEARCH PAGE
$(document).on('keypress', '#page_q', function(e) {
    if (e.which == 13 && $(this).val().length ) {
    $.ajax({url:'/search_page', data:{q:$(this).val()}, async:true,
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
$(document).on('click', '.btn-check-category', function() {
    var catname = $( '#'+$(this).attr('rel') ).val()
    var target = $(this).parent().parent();
    if ( catname.length ) {
      $.ajax({url:'/check_page', data:{page:'Catégorie:'+catname}, async:true,
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
              $('#div-action-move-pages').append(data);
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
              $('#div-action-category').append(data);
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
              //$('#pages').empty();
              //$('#category-to-add').val('');
              $('#div-action-move-category').append(data);
          },
      });
    }
});

