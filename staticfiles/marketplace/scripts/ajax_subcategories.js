function tree(id, url) {
	let element = document.getElementById(id)

	function hasClass(elem, className) {
		return new RegExp("(^|\\s)"+className+"(\\s|$)").test(elem.className)
	}

	function toggleNode(node) {
		let newClass = hasClass(node, 'ExpandOpen') ? 'ExpandClosed' : 'ExpandOpen'
		let re =  /(^|\s)(ExpandOpen|ExpandClosed)(\s|$)/
		node.className = node.className.replace(re, '$1'+newClass+'$3')
	}

	function load(node) {
		function onSuccess(data) {
			if (!data.errcode) {
				onLoaded(data)
				showLoading(false)
			} else {
				showLoading(false)
				onLoadError(data)
			}
		}
		function onAjaxError(xhr, status){
			showLoading(false)

			let errinfo = { errcode: status }
			if (xhr.status != 200) {
				errinfo.message = xhr.statusText
			} else {
				errinfo.message = "Invalid data from the server"
			}
			onLoadError(errinfo)
		}
		function onLoadError(error) {
			let msg = "Error "+error.errcode
			if (error.message) msg = msg + ' :'+error.message
			alert(msg)
		}

		function showLoading(on) {
			let expand = node.getElementsByTagName('DIV')[0]
			expand.className = on ? 'ExpandLoading' : 'Expand'
		}

		function onLoaded(data) {
			for(let i=0; i<data.length; i++) {
				let child = data[i]
				let li = document.createElement('LI')
				li.id = child.id
				li.className = "Node Expand" + (child.is_leaf_node ? 'Leaf' : 'Closed')

				if (i == data.length-1) li.className += ' IsLast'

				li.innerHTML = `
					<div class="Expand"></div>
                          <div class="Content">
                              <a href="${child.absolute_url}">
								  ${child.name} 
                              </a>
                              <sup>(${child.lots_count})</sup>
                          </div>
				`
				if (!child.is_leaf_node) {
					li.innerHTML += '<ul class="Container"></ul>'
				}
				node.getElementsByTagName('UL')[0].appendChild(li)
			}

			node.isLoaded = true
			toggleNode(node)
		}

		showLoading(true)

		$.ajax({
			url: url + node.id,
			method: 'get',
			dataType: 'json',
			success: onSuccess,
			error: onAjaxError,
			cache: false
		})
	}

	element.onclick = function(event) {
		event = event || window.event
		let clickedElem = event.target || event.srcElement

		if (!hasClass(clickedElem, 'Expand')) {
			return
		}

		let node = clickedElem.parentNode

		if (hasClass(node, 'ExpandLeaf')) {
			return
		}

		if (node.isLoaded || node.getElementsByTagName('LI').length) {
			toggleNode(node)
			return
		}


		if (node.getElementsByTagName('LI').length) {
			toggleNode(node)
			return
		}

		load(node)
	}
}
