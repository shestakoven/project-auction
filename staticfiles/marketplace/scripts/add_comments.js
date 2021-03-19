function addComment(parent_id){
    let header_text = "Reply to";
    let parent_comment = document.getElementById(parent_id);
    if (parent_id === "comments"){
        parent_id = "";
        header_text = "Make a comment";
    }
    let lot_id = document.getElementById("lot_id").textContent;
    parent_comment.insertAdjacentHTML(
        'afterend',
        `<div>
          <div class="card mb-4">
            <div class="card-header">${header_text}</div>
            <div class="card-body">
              <form id="comment" action="/api/v1/marketplace/create-comment/" method="post">
                <input type="text" name="text" maxlength="255" class="form-control" required="" id="id_text">
                <select name="parent" id="id_parent" class="visually-hidden">
                  <option value="${parent_id}" selected="${parent_id}"></option>
                </select>
                <input type="text" name="lot" value=${lot_id} required="" id="id_lot" class="visually-hidden">
                <input class="btn btn-primary" type="submit" value="Comment">
              </form>
            </div>
          </div>
        </div>`
    );
    addSubmitAjax()
}

function showNewComment(data){
    let parent_id = data.parent === null ? "comments" : data.parent
    let div = document.createElement('div')
    div.id = data.id
    div.className = "card my-2 p-2"
    div.innerHTML = `
        <div class="d-flex justify-content-between">${ data.user.username }<div></div>${ data.created_at_format }</div>
        <p class="card-text">${ data.text }</p>
    `
    if (data.parent !== null){
        div.innerHTML += `<p>in response to ${ data.parent_data.user_data.username }</p>`
    }

    div.innerHTML += `
        <hr />
        <button type="button" class="btn btn-primary" onclick="addComment(${ data.id })">Reply</button>
    `
    let inner_html = div.innerHTML
    div.innerHTML = `<div class="card-body">${ inner_html }</div>`

    let comments = document.getElementById(parent_id)
    comments.insertAdjacentElement('afterend', div)
}

function onAjaxError(xhr, status){
    let errinfo = { errcode: status }
    if (xhr.status == 403) {
        window.location.replace("/login/");
    } else {
        errinfo.message = "Invalid data from the server"
        onLoadError(errinfo)
    }
}

function onLoadError(error) {
    let msg = "Error "+error.errcode
    if (error.message) msg = msg + ' :'+error.message
    alert(msg)
}

function addSubmitAjax(){
    $('#comment').submit(function() {
        $.ajax({
            headers: {
                'X-CSRFToken': Cookies.get('csrftoken')
            },
            data: $(this).serialize(),
            type: $(this).attr('method'),
            url: $(this).attr('action'),
            success: showNewComment,
            error: onAjaxError
        });
        return false;
    });
}

addSubmitAjax();
