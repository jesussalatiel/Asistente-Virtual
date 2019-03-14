import React, { Component } from 'react';
import axios from 'axios';
import { RouteComponentProps } from 'react-router';
import InvitadoList from './Invitados';


export default class InvitadoDetailView extends Component<RouteComponentProps>{

    constructor(props: RouteComponentProps){
        super(props)
    }
    state = {
        article: {}
    }  
    

    componentDidMount(){
        console.log(this.props.match.params)
        const articleID = 2;

        axios.get(`http://127.0.0.1:8000/api/${articleID}`)
            .then(res => {
                this.setState({
                    article: res.data
                });
                console.log(res.data);
            });
    }
    render(){
        return(
            <div>
                {JSON.stringify(this.state.article)}
            </div>
        )
    }
}


interface Props extends RouteComponentProps<any>{ 
}

export interface RouteComponentProps<P>{
    match: match<P>
}

export interface match<P>{
    params: P;
    esExact: boolean;
    path: any;
    url:string;
}