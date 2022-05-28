const currentPasswordInput = document.querySelectorAll("input[name='current_password']")[0]
const newPasswordInput = document.querySelectorAll("input[name='new_password']")[0]
const confirmPasswordInput = document.querySelectorAll("input[name='confirm_password']")[0]
const csrf = document.querySelectorAll("#reset_pass_form input[name='csrfmiddlewaretoken']")[0]
const resetPassForm = document.getElementById('reset_pass_form')
const toastLiveExample = document.getElementById('liveToast')
// === update profile ====
const updateProfileForm = document.getElementById('update_profile_form')
const fullnameInput = document.querySelectorAll("input[name='fullname']")[0]
const emailInput = document.querySelectorAll("input[name='email']")[0]
const addressInput = document.querySelectorAll("input[name='address']")[0]

resetPassForm.addEventListener('submit' , async (e) => {
    e.preventDefault();
    const currentPassword = currentPasswordInput.value
    const newPassword = newPasswordInput.value
    const confirmPassword = confirmPasswordInput.value
    const csrfToken = csrf.value
    let dataForm = new FormData();
    dataForm.append('current_password', currentPassword);;
    dataForm.append('new_password', newPassword);
    // add form input from hidden input elsewhere on the page
    dataForm.append('csrfmiddlewaretoken', csrfToken);
    if(newPassword !== confirmPassword) {
        // alert('Nhap lai mat khau khong dung')
        const errorConfirmPass = document.getElementById('error_confirm_pass');
        errorConfirmPass.innerText = "Nhập lại mật khẩu không đúng";
    } else {
        let response = await fetch('/profile/password/', {
            method: 'POST',
            body: dataForm,
            credentials: 'same-origin',
        })
        let data = await response.json();
        if(data?.status === 'success') {
            showToast({
                status: 'success',
                announceTitle: 'Chúc mừng',
                message: 'Bạn đã đổi mật khẩu thành công'
            });
        } else {
            showToast({
                status: 'fail',
                announceTitle: 'Xin lỗi',
                message: 'Bạn đã đổi mật khẩu thất bại'
            });
        }
        console.log('data', data);
    }
    console.log('currentPasswordInput', currentPasswordInput.value)
})
updateProfileForm.addEventListener('submit' , async (e) => {
    e.preventDefault();
    const fullname = fullnameInput.value
    const email = emailInput.value
    const address = addressInput.value
    const csrfToken = csrf.value
    let dataForm = new FormData();
    dataForm.append('fullname', fullname);;
    dataForm.append('email', email);
    dataForm.append('address', address);
    // add form input from hidden input elsewhere on the page
    dataForm.append('csrfmiddlewaretoken', csrfToken);
    let response = await fetch('/profile/setProfile', {
        method: 'POST',
        body: dataForm,
        credentials: 'same-origin',
    })
    let data = await response.json();
    if(data?.status === 'success') {
        showToast({
            status: 'success',
            announceTitle: 'Chúc mừng',
            message: 'Bạn đã cập nhật thông tin thành công'
        });
    } else {
        showToast({
            status: 'fail',
            announceTitle: 'Xin lỗi',
            message: 'Bạn đã đổi mật khẩu thất bại'
        });
    }
    console.log('currentPasswordInput', currentPasswordInput.value)
})

const toastTrigger = document.getElementById('liveToastBtn')
const showToast = (data) => {
    const toast = new bootstrap.Toast(toastLiveExample)
    toast.show()
    const toastBody = document.getElementsByClassName('toast-body')[0];
    const announceTitle = document.getElementsByClassName('announceTitle')[0];
    const icon = document.getElementsByClassName('icon-toast')[0];
    console.log('icon', icon)
    toastBody.innerText = data.message
    announceTitle.innerText = data.announceTitle
    if(data.status === 'success') {
        icon.classList.remove('fa-times-circle')
        icon.classList.remove('icon-fail')
        icon.classList.add('fa-check-circle', 'icon-success')
    } else {
        icon.classList.remove('fa-check-circle')
        icon.classList.remove('icon-success')
        icon.classList.add('fa-times-circle', 'icon-fail')
    }
    // if (toastTrigger) {
    //   toastTrigger.addEventListener('click', () => {
    //   })
    // }
}