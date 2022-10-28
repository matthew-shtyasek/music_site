(function music_list() {

$(document).ready(function () { // play music
  let play = true;
  $("#from_pause_to_play")[0].beginElement();
  $('#pause').on('click', function(event) {
    if(play) {
      play = false;
      $("#circle").attr("class", "");l
      $("#from_play_to_pause")[0].beginElement();
    } else {
      play = true;
      $("#circle").attr("class", "play");
      $("#from_pause_to_play")[0].beginElement();
    }
  });
});

let current_song = null;

$(document).ready(function () { // add to playlist
  $('.song-detail .add-song').hover(function () {
    let song_add_dropdown = $('.song-add-dropdown');
    let position = $(this).position();
    song_add_dropdown.css({top: position.top + 40, left: position.left});
    song_add_dropdown.show();
    current_song = $(this).attr('id').split('-')[1];
  });
});

$(document).ready(function () { //hide add to playlist
  $('.song-add-dropdown, .song-detail .add-song').mouseleave(function () {
    if($('.song-add-dropdown:hover').length === 0 && $('.song-detail .add-song:hover').length === 0) {
      let song_add_dropdown = $('.song-add-dropdown');
      song_add_dropdown.css({});
      song_add_dropdown.hide();
    }
  });
});

$(document).ready(function () { //dropdown item click
  let is_dropdown_clicked = false;
  $('.dropdown-item').click(function () {
    if (is_dropdown_clicked)
      return;

    is_dropdown_clicked = true;
    let playlist_id = $(this).attr('id').split('-')[1];

    if (playlist_id === 'create') {
      $.get({
        url: '/profile/create_playlist/',
        success: function (data) {//box-shadow: 5px 5px 5px -1px gray;
          $('body .content').append(`
            <div class="dropdown-window position-absolute flex-box w-25 justify-content-center align-items-center"
                style="z-index: 1;  box-shadow: 5px 5px 5px -1px gray;">
                ${data}
            </div>
          `);
          let classes = $('form.create-playlist').attr('class').replace('w-50', 'w-100');
          $('form.create-playlist').attr('class', classes);
          classes = $('div.create-playlist').attr('class').replace('d-flex', 'flex-column');
          $('div.create-playlist').attr('class', classes);
          $('div.create-playlist').prepend(` 
            <a href="#" class="dropdown-exit-button float-right position-relative">
              &times;
            </a>
          `);


          $('.dropdown-exit-button').click(function () {
            is_dropdown_clicked = false;
            $('.dropdown-window').remove();
          });

          $('.create-playlist').submit(function () {
            $.post({
              url: '/profile/create_playlist/',
              data: $(this).serialize()
            });
            $('.dropdown-exit-button').click();
          });
        }
      });
    } else {
      $.get({
        url: `/profile/add_song/${current_song}/${playlist_id}/`,
      });
    }
  });
});

})();