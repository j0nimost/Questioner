import React, { Component } from 'react'
import { browserHistory, Link } from 'react-router'
import axios from 'axios'
import Cookies from 'universal-cookie'
import './login.css'
import '../styles/style.css'


class LoginUser extends Component {
    constructor() {
        super()
        this.state = {
            email: '',
            password: '',
            hasError: false,
            error: ''
        }
        this.changeHandler = this.changeHandler.bind(this)
        this.submitHandler = this.submitHandler.bind(this)
    }

    componentDidMount() {
        browserHistory.push('/login')
    }

    changeHandler = event => {
        this.setState({
            [event.target.name]: event.target.value
        })
    }

    submitHandler = event => {
        event.preventDefault()

        const payload = {
            'email': this.state.email,
            'password': this.state.password
        }

        axios.post('https://questioneradc36.herokuapp.com/api/v2/auth/signin', payload
        ).then(response => {
            const cookie = new Cookies()
            let timenow = new Date()
            let timelapse = new Date()

            let exptime = timelapse.setDate(timenow.getDay() + 14)

            const token = JSON.stringify(response.data.data["0"].token)
            // console.log(token)
            cookie.set('token', `${token}`, { path: '/', maxAge: exptime })
            console.log('my token ' + cookie.get('token'))
        }).catch(err => {
            this.setState({
                hasError: true,
                error: err.response.data.error
            })
        })

    }


    render() {
        const isError = this.state.hasError
        const err = this.state.error
        return (
            <div className="login">
                <form name="login" onSubmit={this.submitHandler}>
                 
                    {isError ?  <h5 id="error">{err}</h5> : null }

                    <label>Email</label>
                    <input type="email" 
                           name="email" 
                           placeholder="email"
                           value={this.state.email.value}
                           onChange={this.changeHandler} />

                    <label>Password</label>
                    <input type="password" 
                           name="password" 
                           placeholder="Password"
                           value={this.state.password.value} 
                           onChange={this.changeHandler}/>
                    <input type="submit" value="Submit"/>
                    <Link to='/' id="link">or Sign up?</Link>
                </form>
            </div>
        )
    }
}

export default LoginUser