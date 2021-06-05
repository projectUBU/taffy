// console.log('hello world')

// get all the stars
const one = document.getElementById('first')
const two = document.getElementById('second')
const three = document.getElementById('third')
const four = document.getElementById('fourth')
const five = document.getElementById('fifth')
// console.log(one,)


// get the form, confirm-box and csrf token
const form = document.querySelector('.rate-form')
const confirmBox = document.getElementById('confirm-box')
const csrf = document.getElementsByName('csrfmiddlewaretoken')
const confirmrejected = document.getElementById('confirm-rejected')

// console.log(form)
// console.log(confirmBox)
// console.log(csrf)

const handleStarSelect = (size) => {
    const children = form.children
    // console.log(children[0])
    for (let i=0; i < children.length; i++) {
        if(i <= size) {
            children[i].classList.add('checked')
        } else {
            children[i].classList.remove('checked')
        }
    }
}

const handleSelect = (selection) => {
    switch(selection){
        case 'first': {
            // one.classList.add('checked')
            // two.classList.remove('checked')
            // three.classList.remove('checked')
            // four.classList.remove('checked')
            // five.classList.remove('checked')
            handleStarSelect(1)
            return
        }
        case 'second': {
            handleStarSelect(2)
            return
        }
        case 'third': {
            handleStarSelect(3)
            return
        }
        case 'fourth': {
            handleStarSelect(4)
            return
        }
        case 'fifth': {
            handleStarSelect(5)
            return
        }
        default: {
            handleStarSelect(0)
        }
    }

}

const getNumericValue = (stringValue) =>{
    let numericValue;
    if (stringValue === 'first') {
        numericValue = 1
    } 
    else if (stringValue === 'second') {
        numericValue = 2
    }
    else if (stringValue === 'third') {
        numericValue = 3
    }
    else if (stringValue === 'fourth') {
        numericValue = 4
    }
    else if (stringValue === 'fifth') {
        numericValue = 5
    }
    else {
        numericValue = 0
    }
    return numericValue
}

if (one) {
    const arr = [one, two, three, four, five]

    arr.forEach(item=> item.addEventListener('mouseover', (event)=>{
        handleSelect(event.target.id)
    }))

    arr.forEach(item=> item.addEventListener('click', (event)=>{
        // value of the rating not numeric
        const val = event.target.id
        console.log(val)
        
        let isSubmit = false
        form.addEventListener('submit', e=>{
            e.preventDefault()
            if (isSubmit) {
                return
            }
            isSubmit = true
            // picture id
            const req_id =  e.target.name
            const id = e.target.id
            console.log(id)
            console.log(req_id)
            // value of the rating translated into numeric
            const val_num = getNumericValue(val)

            $.ajax({
                type: 'POST',
                url: '/dm/rate/',
                data: {
                    'csrfmiddlewaretoken': csrf[0].value,

                    'req_id':req_id ,
                    'mx_id': id,
                    'val': val_num,
                },
                success: function(response){
                    console.log(response)
                    confirmBox.innerHTML = `<span>Successfully rated with ${response.score}</span>`
                    confirmrejected.innerHTML = `<button  type="button" class="btn btn-outline-danger btn-lg btn-block rounded-pill"  
                    data-toggle="modal" data-target="#modal-notification"  data-backdrop="static" data-keyboard="false" ><i class="fa fa-user-times"></i>&nbsp;ทำการปฏิเสทเนื้อคู่ของคุณ</button>`
                },
                error: function(error){
                    console.log(error)
                    confirmBox.innerHTML = '<span>Ups... something went wrong</span>'
                    confirmrejected.innerHTML = `<button disabled = "disabled" type="button" class="btn btn-outline-danger btn-lg btn-block rounded-pill"  
                    data-toggle="modal" data-target="#modal-notification"  data-backdrop="static" data-keyboard="false" ><i class="fa fa-user-times"></i>&nbsp;ทำการปฏิเสทเนื้อคู่ของคุณ</button>`
                }
            })
        })
    }))
}