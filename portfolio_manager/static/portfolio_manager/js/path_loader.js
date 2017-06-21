$(function() {

  function change_if_all_selected() {
    var xIsChosen = $('#x-selector').val() != '---',
        yIsChosen = $('#y-selector').val() != '---',
        projectIsChosen = $('#r-selector').val() != '---';

    if (xIsChosen && yIsChosen && projectIsChosen) {
      dimension_selector_change();
    }
    return;
  }

  function dimension_selector_change() {
    x_dimension_id = $('#x-selector').find("option:selected").val();
    y_dimension_id = $('#y-selector').find("option:selected").val();

    selected_project = get_selected_project();

    update_path_visualization(
      get_dimension(selected_project, x_dimension_id),
      get_dimension(selected_project, y_dimension_id)
    );
  }

  $.ajax({
    url: "json"
  }).done(function(data) {
    db_json = data;
    for (var i = 0, len = data.length; i < len; i++) {
      $('#project-selector').append('<option value="'+data[i].id+'">'+data[i].name+'</option>')
      $('#project-selector').prop('disabled', false);
    }
  });

  $('#project-selector').on('change', function() {
    project_id = $(this).find("option:selected").val();

    preserved_x_name = $('#x-selector').find("option:selected").text();
    preserved_y_name = $('#y-selector').find("option:selected").text();

    $('#x-selector').html('<option>---</option>');
    $('#y-selector').html('<option>---</option>');

    for (var i = 0, len = db_json.length; i < len; i++) {
      if(db_json[i].id == project_id) {
        project = db_json[i];
        for (var j = 0; j < project.dimensions.length; j++) {
          if('history' in project.dimensions[j].dimension_object) {
            $('#x-selector').append('<option value="'+project.dimensions[j].id+'">'+project.dimensions[j].dimension_object.name+'</option>');
            $('#x-selector').prop('disabled', false);
            if (project.dimensions[j].dimension_type == 'DecimalDimension') {
              $('#y-selector').append('<option value="'+project.dimensions[j].id+'">'+project.dimensions[j].dimension_object.name+'</option>');
              $('#y-selector').prop('disabled', false);
            }
          }
        }
        break;
      }
    }

    var y_id = null;
    $('#y-selector').children().each(function(i, option) {
      if (option.value != '---'
          && (option.text == preserved_y_name || y_id == null))
        y_id = option.value;
    });
    if (y_id != null)
      $('#y-selector').val(y_id);

    var x_id = null;
    $('#x-selector').children().each(function(i, option) {
      if (option.value != '---'
          && (option.text == preserved_x_name
              || (x_id == null && option.value != y_id)))
        x_id = option.value;
    });
    if (x_id != null)
      $('#x-selector').val(x_id);

    change_if_all_selected();
  });

  $('#x-selector').on('change', change_if_all_selected);
  $('#y-selector').on('change', change_if_all_selected);

});