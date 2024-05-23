$(document).ready(function () {
  $(".like-button").click(function (event) {
    event.preventDefault();
    var postID = $(this).data("post-id");
    likePost(postID);
  });

  function likePost(postID) {
    $.get(`/likePost?post_id=${postID}`, function (data) {
      // Cập nhật UI tùy thuộc vào phản hồi từ server
      if (data.success) {
        $("#like-count-" + postID).text(data.like_count);
        var likeText = data.like_count === 1 ? "like" : "likes";
        $("#like-text-" + postID).text(likeText);
      } else {
        console.error("Failed to like post.");
      }
    });
  }
});
