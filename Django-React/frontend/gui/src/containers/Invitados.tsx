import React, { Component } from 'react';
import axios from 'axios';

class InvitadoList extends Component {
    
    state = {
        articles: []
    }

    componentDidMount(){
        axios.get('http://127.0.0.1:8000/api/')
        .then( res =>{
            this.setState({
                articles : res.data
            });
            console.log(res.data);
        });
        
    }

    render(){
        return(
            <div>
                {JSON.stringify(this.state.articles)}
            </div>
        )
    }
}

export default InvitadoList;