$(document).ready(function () {
  $(".like-button-cmt").click(function (event) {
    event.preventDefault();
    var commentID = $(this).data("comment-id");
    likeComment(commentID);
  });

  function likeComment(commentID) {
    $.get(`/likeComment?comment_id=${commentID}`, function (data) {
      // Cập nhật UI tùy thuộc vào phản hồi từ server
      if (data.success) {
        $("#like-cmt-count-" + commentID).text(data.like_count);
        var likeText = data.like_count === 1 ? "like" : "likes";
        $("#like-cmt-text-" + postID).text(likeText);
      } else {
        console.error("Failed to like comment.");
      }
    });
  }
});
