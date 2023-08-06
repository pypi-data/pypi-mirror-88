import React from 'react';
import Pin from '../assets/caption-pin.svg';
import Call from '../assets/caption-call.svg';
import Email from '../assets/caption-email.svg';
import Next from '../assets/next.svg';


function FamilyCard(props) {
    console.log(props.item)
    return(
        <div  style={{  }}   className="offer-card">
            <div className="card-container-img">
                <a href={"num" && props.infoUrl + props.item["offer"]["offerID"]+'&type='+props.item["offer"]["offerTypeId"]} target="_blank"> 
                    <img className="embed-responsive-img offer-card-img" variant="top" src={"https://pivotweb.tourismewallonie.be/PivotWeb-3.1/img/" + props.item["offer"]["offerID"] } />
                </a>
            </div>
            <div className="card-caption">
                <a className='card-caption-title' href={"num" && props.infoUrl + props.item["offer"]["offerID"]+'&type='+props.item["offer"]["offerTypeId"]} target="_blank">{props.item["title"]}</a>
                

                {props.item["phone"] ?
                    <span className='card-caption-num'>
                        <img className='card-icon' src={Call} alt="Logo pin" />
                        <a href={"tel:"+props.item["phone"]}>{props.item["phone"]}</a>
                    </span>
                    :""} 

                {props.item["email"] ?
                    <span className='card-caption-email'>
                        <img className='card-icon' src={Email} alt="Logo pin" />
                        <a href={"mailto:"+props.item["email"]}>{props.item["email"]}</a>
                    </span>
                :""}
                {props.item["cp"] ? 
                    <span className='card-caption-cp'>
                        <img className='card-icon' src={Pin} alt="Logo pin" /> 
                        {props.item["cp"]}
                    </span>
                :""}

               <span className='card-caption-details'>
                    <a href={"num" && props.infoUrl + props.item["offer"]["offerID"]+'&type='+props.item["offer"]["offerTypeId"]} target="_blank">Détails</a>
                    <img className='card-next' src={Next} alt="Logo pin" /> 
                </span>
            </div>
        </div>
    );
}
export default FamilyCard;