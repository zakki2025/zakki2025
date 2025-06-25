import axios from 'axios'

const service =  axios.create({
    baseURL: '/api',
    timeout: 12000,
    headers: {
        'Content-Type': 'application/json'
    }
})

export default service


