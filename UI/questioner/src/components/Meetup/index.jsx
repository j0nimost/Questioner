import React, { Component } from 'react'
import { browserHistory } from 'react-router'
import axios from 'axios'
import axiosRetry from 'axios-retry'
import { Cookies } from 'react-cookie'
import './meetup.css'


class Meetup extends Component {

    constructor(props) {
        super(props)

        const cookie = new Cookies()
        this.state = {
            token: cookie.get('token') || '',
            meetups: [],
            hasError: false,
            error: ''
        }
    }

    componentDidMount = () => {
        this.getallHandler()
        browserHistory.push('/')
    }

    getallHandler = () => {
        const upcoming_meetups = 'https://questioneradc36.herokuapp.com/api/v2/meetups/upcoming'
        axiosRetry(axios, { retries: 5 });

        axios.get(upcoming_meetups, { headers: { "Authorization": `Bearer ${this.state.token}` } }
        ).then((response) => {
            let arr_meetups = []
            arr_meetups = response.data.data
            console.log(typeof arr_meetups)
            this.setState({
                meetups: arr_meetups
            })
            console.log('meetups \n' + JSON.stringify(arr_meetups))
        }).catch((err) => {
            if (!err.response) {
                console.log(err)
            }
            else {
                const response_err = JSON.stringify(err.response.data.error)
                console.log(response_err)

                this.setState({
                    hasError: true,
                    error: response_err,
                })
                browserHistory.push('/login')
            }
        })
    }

    render() {

        let meetups = this.state.meetups

        return (
            <div className="meetup">
                <div className="meetup-list">
                    <ul>
                        {meetups.map(meetup => <MeetupsList key={meetup.id} meetup={meetup} />)}
                    </ul>
                </div>
                <div className="info">
                    <div className="meetup-types">
                        <ul>
                            <li className="active"><span>All Meetups</span></li>
                            <li><span>My Meetups</span></li>
                            <li><span>Attending</span></li>
                        </ul>
                    </div>
                </div>
            </div>
        )
    }
}


const MeetupsList = ({ meetup }) => {
    return (
        <li id='list-item'>
            <div className="meetup-inline">

                <div id="time">
                    <h4>{meetup.happeningon}</h4>
                </div>
                <div id="meetup-body">
                    <div>
                        {meetup.tags ? <ul>{meetup.tags.map(tg => <TagList key={tg} tag={tg} />)}</ul> : null}
                        <span id="scheduled"><img src="https://img.icons8.com/ios/50/000000/alarm.png" alt="scheduled" /></span>
                        <div>
                            <a href="meetup.html" id="title">
                                <h3>{meetup.topic}</h3>
                            </a>
                            <p>{meetup.venue}</p>
                        </div>
                    </div>
                </div>
            </div>
        </li>
    )
}


const TagList = ({ tag }) => {
    const listStyle = {
        display: 'inline-block',
        padding: 2
    }
    return (
        <li style={listStyle}>
            <a href='#tag' id='tag'>
                <h5>#{tag}</h5>
            </a>
        </li>
    )
}

export default Meetup