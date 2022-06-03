let detailBillBtns = [...document.getElementsByClassName('detail_bill_btn')]
let wpDetailBill = document.getElementsByClassName('wp_detail_bill')[0]
let previousBtn = document.querySelectorAll('a[aria-label="Previous"]')[0]
let nextBtn = document.querySelectorAll('a[aria-label="Next"]')[0]
const pageItemNumbers = [...document.getElementsByClassName('page-item-number')]
const host = 'http://127.0.0.1:8000/'
const url = window.location.href
let currentPage = url.split('?').pop().split('=').pop();
// alert(currentPage)
if(currentPage === '1' || isNaN(currentPage)) {
    previousBtn.style.display = 'none'
} else {
    previousBtn.style.display = 'inline-block'
}
if(currentPage === pageItemNumbers.length.toString()) {
    nextBtn.style.display = 'none'
} else {
    nextBtn.style.display = 'inline-block'
}
console.log('page', currentPage)
console.log('previoustBtn', previousBtn)
const formatMoney = (number) => {
    let x = number.toLocaleString('it-IT', {style : 'currency', currency : 'VND'});
    console.log(x);
    return x
}
detailBillBtns.forEach((btn) => {
    btn.addEventListener('click', async (e) => {
        let billCode = e.target.dataset.billCode
        let response =await fetch(`/listbill/detail?billCode=${billCode}`)
        let data = await response.json();
        console.log('data', data)
        let total = 0;
        let status = {};
        if(data.status === 0) {
            status = {
                text: 'Đang xử lí',
                class: 'text-bg-secondary'
            }
        }
        else if(data.status === 1) {
            status = {
                text: 'Đang giao hàng',
                class: 'text-bg-warning'
            }
        }
        else {
            status = {
                text: 'Đã giao hàng',
                class: 'text-bg-success'
            }
        };
        let html = `
        <h5>Mã đơn hàng: ${data?.billCode}</h5>
        <div class='d-flex align-items-center gap-3 mb-2'>
            <h5 class="m-0">Trạng thái: </h5>
            <span class="badge ${status.class}">${status.text}</span>
        </div>
        <h5>Danh sách sản phẩm</h5>
        <table class="table">
            <thead>
                <tr>
                <th scope="col">#</th>
                <th scope="col">Tên sản phẩm</th>
                <th scope="col">Giá tiền</th>
                <th scope="col">Số lượng</th>
                <th scope="col">Thành tiền</th>
                <th></th>
                </tr>
            </thead>
            <tbody>
        `
        data?.arr_items?.forEach((item, index) => {
            total += item.price*item.quantity
            html += `
                <tr>
                <th scope="row">${index+1}</th>
                <td>
                    ${item?.name_food}
                </td>
                <td>
                    ${formatMoney(parseInt(item?.price, 10))}
                </td>
                <td>
                    ${item?.quantity}
                </td>
                <td>
                    ${formatMoney(parseInt(item?.price*item?.quantity, 10))}
                </td>
            </tr>
            `
        })
        html += `
            </tbody>
        </table>
        <h5>Địa chỉ: ${data.address}</h5>
        <h5 class='fw-bold'>Tổng tiền: ${formatMoney(parseInt(total))}</h5>
        `
        wpDetailBill.innerHTML = html;
        console.log('data', data)
    })
})
pageItemNumbers.forEach((item) => {
    let pageNumber = item.dataset.pageNumber
    if(isNaN(currentPage)) {
        pageItemNumbers[0].classList.add('active')
    }
    if(pageNumber.toString() === currentPage.toString()) {
        item.classList.add('active')
    }
})
previousBtn.addEventListener('click', (e) => {
    // const listBillURL = host + 'listbill'
    const listBillURL = '/listbill'
    let newURL = listBillURL + `?page=${parseInt(currentPage, 10)-1}`
    window.location.replace(newURL);
})
nextBtn.addEventListener('click', (e) => {
    // const listBillURL = host + 'listbill'
    const listBillURL = '/listbill'
    let newURL = listBillURL + `?page=${parseInt(currentPage, 10)+1}`
    window.location.replace(newURL);
})