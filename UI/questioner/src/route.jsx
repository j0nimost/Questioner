import React from 'react'
import { Route, IndexRoute } from 'react-router'
import App from './App'
import RegisterUser from './components/Register/index'
import LoginUser from './components/Login/index'
import Meetup from './components/Meetup/index'

export default(
    <Route path='/' component={App}>
    <IndexRoute component={Meetup} />
    <Route path='/login' component={LoginUser} />
    <Route path='/register' component={RegisterUser}/>
    <Route path='*' component={Meetup} />
  </Route>
)