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
  $('.dropdown-item').click(function () {
    let playlist_id = $(this).attr('id').split('-')[1];

    if (playlist_id === 'create') {

    } else {
      $.get(`/add_song/${current_song}/${playlist_id}/`);
    }
  });
});

})();