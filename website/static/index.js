function deleteNote(noteId) {
	fetch('/delete-note', { //send POST request to /delete-note route
		method: 'POST',
		body: JSON.stringify({ noteId: noteId}) //sends string with note id
	}).then((_res) => {
		window.location.href = "/"; //reload window with GET request after response
	});
}