import React from 'react'
import { Route, IndexRoute } from 'react-router'
import App from './App'
import RegisterUser from './components/Register/index'

export default(
    <Route path='/' component={App}>
    <IndexRoute component={RegisterUser} />
    <Route path='*' component={RegisterUser} />
  </Route>
)