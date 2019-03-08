import React, { Component } from 'react'
import { browserHistory, Link } from 'react-router'
import axios from 'axios'
import { Cookies } from 'react-cookie'
import './register.css'
import '../styles/style.css'

class RegisterUser extends Component {
    constructor(props) {
        super(props)
        this.state = {
            fullname: '',
            email: '',
            username: '',
            password: '',
            confirmpassword: '',
            hasError: false,
            error: ''
            }
        
        this.changeHandler = this.changeHandler.bind(this)
        this.submitHandler = this.submitHandler.bind(this)/**/
    }

    componentDidMount() {
        browserHistory.push('/')
    }

    changeHandler = event => {
        this.setState({
            [event.target.name]: event.target.value
        })
    }

    submitHandler = event => {
        event.preventDefault()

        const payload = {
            "fullname": this.state.fullname,
            "email": this.state.email,
            "username": this.state.username,
            "password": this.state.password,
            "confirmpassword": this.state.confirmpassword
        }

        axios.post('https://questioneradc36.herokuapp.com/api/v2/auth/signup', payload
        ).then( response => {
                // set cookie
                const cookie = new Cookies()

            const token = response.data.data["0"].token
            cookie.set('token', `${token}`, { path: '/', maxAge: exptime })
            console.log('cookie created')
        }).catch(error => {
            this.setState({
                hasError: true,
                error: error.response.data.error
            })
        })
    }

    render() {
        const isError = this.state.hasError
        const err = this.state.error.toUpperCase()
        return (
            <div className="register">
                <form name="register" onSubmit={this.submitHandler}>
                
                { isError ? <h5 id="error">{err}</h5> : null}
                    <label>Fullname</label>
                    <input type="text"
                        name="fullname"
                        placeholder="Fullname"
                        value={this.state.fullname.value}
                        onChange={this.changeHandler} />

                    <label>Email</label>
                    <input type="email"
                        name="email"
                        placeholder="Email"
                        value={this.state.email.value}
                        onChange={this.changeHandler} />

                    <label>Username</label>
                    <input type="text"
                        name="username"
                        placeholder="Username"
                        value={this.state.username.value}
                        onChange={this.changeHandler} />

                    <label>Password</label>
                    <input type="password"
                        name="password"
                        placeholder="Password"
                        value={this.state.password.value}
                        onChange={this.changeHandler} />

                    <label>Confirm Password</label>
                    <input type="password"
                        name="confirmpassword"
                        placeholder="Confirm Password"
                        value={this.state.confirmpassword.value}
                        onChange={this.changeHandler} />

                    <input type="submit" value="Submit" />
                    <Link to='/login' id='link'>or Sign in?</Link>
                </form>
            </div>
        )
    }
}


export default RegisterUser