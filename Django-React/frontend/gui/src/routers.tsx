import React from 'react';
import { Route } from 'react-router-dom';

import InvitadoList from './containers/Invitados';
import InvitadoDetailView from './containers/InvitadoDetailView';

const BaseRouter = () => {
    return(
    <div>
        <Route exact path = "/" component = {InvitadoList}></Route>
        <Route path="/:invitadoID" component={InvitadoDetailView}></Route>

    </div>
    )
}

export default BaseRouter;