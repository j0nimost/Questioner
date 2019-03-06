import React, { Component } from 'react'
import '../styles/style.css'

class Navbar extends Component {
    constructor(props) {
        super(props)
        this.state = { isLoggedIn: true, }
    }

    render() {
        const isLoggedin = this.state.isLoggedIn
        return (
            <nav>
                <ul>
                    <li id="logo">
                        <a href="#index">
                            <img src="https://svgshare.com/i/BWN.svg" alt="logo">
                            </img>
                        </a>
                    </li>
                    { isLoggedin ? (<li id="profile_logo">
                        <a href="#profile">
                             <profileIcon className="profileIcon"/> 
                        </a>
                    </li>) : null}
                </ul>
            </nav>
        )
    }
}

const profileIcon = ({isLoggedin}) => {
    return (
        <img src='' alt='profile' />
    )
}

export default Navbar