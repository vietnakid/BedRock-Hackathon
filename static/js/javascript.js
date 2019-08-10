$(document).ready(function(){
    // When user click add button on table
    var counter = $('#total_form').val();
    $('#add').click(function(){
        counter++;
        var form = `
        <tr id="row-${counter}">
        <td>Form name: <input name="form-name-${counter}" type="text" value=""></td>
        <td>Input type:<br>
          <input type="radio" name="input-type-${counter}" class="radInp" value="text" data-id="${counter}" checked> Text<br>
          <input type="radio" name="input-type-${counter}" class="radInp" value="radio" data-id="${counter}"> Radio<br>
          <input type="radio" name="input-type-${counter}" class="radInp" value="checkbox" data-id="${counter}"> Checkbox<br>
          <input type="radio" name="input-type-${counter}" class="radInp" value="multiline_text" data-id="${counter}"> Multiline Text<br>
        </td>
        <td>
          <div id='display-data-${counter}'>
              <button class="btn btn-primary" data-method="getData" data-option="" data-target="#putData-${counter}" type="button">
              <span class="docs-tooltip" data-toggle="tooltip" title="$().cropper("getData")">Get Data</span>
              </button>
              <input name="form-possition-${counter}" class="form-control" id="putData-${counter}" type="text" placeholder="Get Pixel">
          </div>
        </td>
        <td><button type="button" name="remove" id="remove-${counter}" data-id="${counter}" class="btn btn-danger btn_remove">X</button></td>
     </tr>
        `
        $('#dynamic_field').append(form);
    });
    
    // When user click remove button on table
    $(document).on('click', '.btn_remove', function(){
    // $("[id^=remove-]").click(function(){
        var button_id = $(this).attr("data-id"); 
        console.log($('#row-'+button_id))
        $('#row-'+button_id).remove();
    });
    
    // When user click submit button
    $('#submit').click(function(){		
      $.ajax({
        url:"name.php",
        method:"POST",
        data:$('#add_name').serialize(),
        success:function(data)
        {
          alert(data);
          $('#add_name')[0].reset();
        }
      });
    });

    // Type Selected
    // $("input[name^=input-type-]").change(function(){
    $(document).on('change', '.radInp', function(){
        data_id = $(this).attr('data-id');
        value = $(this).attr('value');
        div_display_data = $("#display-data-"+data_id)
        console.log(data_id + value)
        // console.log(div_display_data.html)
        if (value == "text" || (value == "multiline_text")) {
            form = `
            <button class="btn btn-primary" data-method="getData" data-option="" data-target="#putData-${data_id}" type="button">
            <span class="docs-tooltip" data-toggle="tooltip" title="$().cropper("getData")">Get Data</span>
            </button>
            <input name="form-possition-${data_id}" class="form-control" id="putData-${data_id}" type="text" placeholder="Get Pixel"></input>
            `
            div_display_data.html(form);
        } else if (value == "radio" || value == "checkbox") {
            form = `
            <table id='table-data-${data_id}'>
            <tr id='row-data-${data_id}-1'>
                <td>
                <button class="btn btn-primary" data-method="getData" data-option="" data-target="#putData-${data_id}-1" type="button">
                <span class="docs-tooltip" data-toggle="tooltip" title="$().cropper("getData")">Get Data</span>
                </button>
                <input name="form-possition-${data_id}-1" class="form-control" id="putData-${data_id}-1" type="text" placeholder="Get Pixel">
                </td>
                <td><button type="button" name="remove" id="remove-choice-${data_id}-1" data-id="${data_id}-1" class="btn btn-danger btn-rad-rm">X</button></td>
            </tr>
            <tr id='row-data-${data_id}-2'>
                <td>
                <button class="btn btn-primary" data-method="getData" data-option="" data-target="#putData-${data_id}-2" type="button">
                    <span class="docs-tooltip" data-toggle="tooltip" title="$().cropper("getData")">Get Data</span>
                    </button>
                    <input name="form-possition-${data_id}-2" class="form-control" id="putData-${data_id}-2" type="text" placeholder="Get Pixel">
                </td>
                <td><button type="button" name="remove" id="remove-choice-${data_id}-2" data-id="${data_id}-2" class="btn btn-danger btn-rad-rm">X</button></td>
            </tr>
            </table>
            <button type="button" name="add" id="add-choice-${data_id}" data-id="${data_id}" class="btn btn-success btn-red-add">Add More Row</button>
            `
            div_display_data.html(form);
        }
    });

    // When user add more choice to a radio field
    $(document).on('click', '.btn-red-add', function(){
        data_id = $(this).attr('data-id');
        table_display_data = $("#table-data-"+data_id)
        console.log(table_display_data)
        counter++;
        var form = `
        <tr id='row-data-${data_id}-${counter}'>
        <td>
            <button class="btn btn-primary" data-method="getData" data-option="" data-target="#putData-${data_id}-${counter}" type="button">
                <span class="docs-tooltip" data-toggle="tooltip" title="$().cropper("getData")">Get Data</span>
                </button>
                <input name="form-possition-${data_id}-${counter}" class="form-control" id="putData-${data_id}-${counter}" type="text" placeholder="Get Pixel">
        </td>
        <td><button type="button" name="remove" id="remove-choice-${data_id}-${counter}" data-id="${data_id}-${counter}" class="btn btn-danger btn-rad-rm">X</button></td>
        </tr>
        `
        table_display_data.append(form);
    });

    // When user remove a choice to a radio field
    $(document).on('click', '.btn-rad-rm', function(){
        data_id = $(this).attr('data-id');
        deleted_row = $("#row-data-"+data_id)
        console.log(deleted_row)
        deleted_row.remove();
    });
    
  });

  