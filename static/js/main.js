function showMessage(status, title, errorMessage) {
    Swal.fire({
        icon: status,
        title: title,
        text: errorMessage,
    }).then(function(result) {
        if (result.isConfirmed) {
            window.location.reload();
        }
    });;
}