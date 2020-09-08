const table = document.querySelector('#table_waiting');
var tbody= table.querySelector('tbody');
const dragObj = {index: null};
const exchangeObj = {index: null};
// const dragObj = { nextObj: null, target: null, index: null, main_app: null};
// const exchangeObj = { nextObj: null, target: null, index: null, main_app: null};

function inserElem(dragObj, position) {
    // if (dragObj.index == position.index) {
    //     console.log('no change');
    //     return;
    // } else if (dragObj.index > position.index){
    //     // nextObj没有说明与最后一个元素做交换
    //     tbody.insertBefore(dragObj.target, position.target);
    // } else{
    //     if (position.nextObj === null) {
    //         console.log('exchange to last');
    //         tbody.appendChild(dragObj.target);
    //     } else {
    //         //　将现在这个元素插入到需要交换的前一个元素之前
    //         // 这里对于同元素的insertBefore会直接执行在原来节点内元素的删除和新节点内元素的append不需要手动操作
    //         console.log(tbody);
    //         tbody.insertBefore(dragObj.target, position.nextObj);
    //     }
    // };
    $.ajax({
        url: '/test',
        type: 'get',
        data: {drag_rowIndex: dragObj.index, target_rowIndex: exchangeObj.index},
        success: function (data) {
            alert('更改成功');
        },
        error: function (e) {
            alert('连接异常');
        },
    });

};

// 记录目前正在拖动的元素
table.ondragstart = event => {
    dragObj.index = event.target.rowIndex;
    // dragObj.target = event.target;
    // dragObj.index= event.target.rowIndex;
    // dragObj.main_app = event.target.cells[3].innerText;
    // dragObj.nextObj = event.target.nextElementSibling;
    // dragObj.main_app = event.target.
    // console.log("dragObj:" + dragObj.nextObj + "," + dragObj.target);
};

table.ondragover = event => {
    event.preventDefault();
    // exchangeObj.target = event.target.parentElement;
    // exchangeObj.index = event.target.parentElement.rowIndex;
    // exchangeObj.main_app = event.target.parentElement.cells[3].innerText;
    // exchangeObj.nextObj = event.target.parentElement.nextElementSibling;

};

table.ondragend = event => {
    // if (exchangeObj.target && dragObj.target) {
    //     inserElem(dragObj, exchangeObj);
    //     // inserElem(exchangeObj, dragObj);
    // }
};

table.ondrop = event => {
    // console.log("exchangeObj:" + exchangeObj.nextObj + "," + exchangeObj.target);
    exchangeObj.index = event.target.parentElement.rowIndex;
    // exchangeObj.target = event.target.parentElement;
    // exchangeObj.nextObj = event.target.parentElement.nextElementSibling;
    var csrf = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url: '/test/',
        type: 'post',
        data: {drag_rowIndex: dragObj.index, target_rowIndex: exchangeObj.index, csrfmiddlewaretoken:csrf},
        success: function (data) {
            alert('更改成功');
        },
        error: function (e) {
            alert('连接异常');
        },
    });
};
