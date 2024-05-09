$(document).ready(function(){
    // Function to handle Add Course button click
    $('#addCourse').click(function(){
        $('#classModal').modal('show');
        $('#classForm')[0].reset();        
        $('.modal-title').html("<i class='fa fa-plus'></i> Add Course");
        $('#action').val('addCourse');
        $('#save').val('Add Course');
    });     

    // Function to handle Edit Course button click
    $(document).off('click', '.editCourse').on('click', '.editCourse', function(){
        $('#editModal').modal('show');

        // Get course details from the button data attributes
        var courseId = $(this).data('course-id');
        var courseName = $(this).data('course-name');
        var lecturerId = $(this).data('lecturer-id');

        // Set the values in the edit modal form
        $('#edit-cid').val(courseId);
        $('#edit-cname').val(courseName);
        $('#edit-lecturer').val(lecturerId);

        // Update modal title and button text
        $('.edit-title').html("<i class='fa fa-pencil'></i> Edit Course");
        $('#edit-save').val('Save Changes');
    }); 

    // Function to handle form submission in edit modal
    $('#editForm').submit(function(e) {
        e.preventDefault(); // Prevent form submission

        // Get form data
        var formData = {
            edit_cid: $('#edit-cid').val(),
            edit_cname: $('#edit-cname').val(),
            edit_lecturer: $('#edit-lecturer').val(),
            action: 'editCourse' // Assuming this is how you identify the action in your form
        };

        // Send AJAX request to save the changes
        $.ajax({
            type: 'POST',
            url: '/save_course', // Modify the URL as per your Flask route
            data: formData,
            success: function(response) {
                // Handle success response (if needed)
                // For example, you can close the modal and show a success message
                $('#editModal').modal('hide');
                alert('Course updated successfully');
                // Reload the page to reflect the changes
                window.location.reload();
            },
            error: function(xhr, status, error) {
                // Handle error response (if needed)
                // For example, you can display an error message
                alert('An error occurred while updating the course');
            }
        });
    });

    // Function to handle form submission in search form
    $('#searchForm').submit(function(e) {
        e.preventDefault(); // Prevent form submission

        var searchQuery = $('#searchQuery').val();

        $.ajax({
            type: 'GET',
            url: '/search', // Modify the URL as per your Flask route
            data: { query: searchQuery },
            success: function(response) {
                // Display search results
                $('#searchForm').html(response);
            },
            error: function(xhr, status, error) {
                // Handle error response (if needed)
                console.error(error);
            }
        });
    });
});
