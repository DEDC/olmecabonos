document.addEventListener('DOMContentLoaded', function () {
    let form = document.querySelector('#check');
    let name = document.querySelector('#ab-name')
    let section = document.querySelector('#ab-section')
    let row = document.querySelector('#ab-row')
    let seat = document.querySelector('#ab-seat')
    let hold = document.querySelector('#hold')
    let input = document.querySelector('#bonus')
    let input2 = document.querySelector('#game')

    input.addEventListener('change', (e) => {
        axios({
            method: 'post',
            url: '/check/bonus',
            data:{bonus: input.value, partido: input2.value}
        }).then(function (response) {
            let data = response.data;
            name.textContent = data.person.name
            row.textContent = data.ubication.row
            section.textContent = data.ubication.section
            seat.textContent = data.ubication.seat
            if (data.created) {
                hold.classList.remove('border-warning')
                hold.classList.remove('border-success')
                hold.classList.add('border-success')
            }
            else {
                hold.classList.add('border-success')
                hold.classList.remove('border-warning')
                hold.classList.add('border-warning')
            }
        }).catch(function (error) {
            console.log(error)
            // hold.classList.add('border-danger')
        })
        input.value = ''
    })

    // form.addEventListener('submit', (e) => {
    //     e.preventDefault();
    //     const data = new FormData(e.target)
    //     axios({
    //         method: 'post',
    //         url: '/check/bonus',
    //         data
    //     }).then(function (response) {
    //         let data = response.data;
    //         name.textContent = data.person.name
    //         row.textContent = data.ubication.row
    //         section.textContent = data.ubication.section
    //         seat.textContent = data.ubication.seat
    //         if (data.created) {
    //             hold.classList.remove('border-warning')
    //             hold.classList.remove('border-success')
    //             hold.classList.add('border-success')
    //         }
    //         else {
    //             hold.classList.add('border-success')
    //             hold.classList.remove('border-warning')
    //             hold.classList.add('border-warning')
    //         }
    //     }).catch(function (error) {
    //         console.error(error);
    //     })
    //     form.reset();
    // })
})