$(".delete-round").click(deleteRound);

async function deleteRound() {
  const id = $(this).data("id");
  await axios.delete(`/delete_round/${id}`);
  $(this).parent().remove();
}
