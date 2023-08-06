import React, {useState, useEffect} from 'react';
import { Map, TileLayer, Marker, Popup } from 'react-leaflet';
import L from 'leaflet';
import iconSvg from '../assets/pin.svg';

function FamilyMap(props) {
  const [activeItem, setActiveItem] = useState(null);
  const [firstLat, setFirstLat] = useState(50.44569);
  const [firstLong, setFirstLong] = useState(3.95355);



  var mapIcon = L.icon({
    iconUrl: iconSvg,
    iconSize:     [38, 95], // size of the icon

});


  useEffect(() => {
    if(props.items !== null){
      setFirstLat(props.items[0].latitude)
      setFirstLong(props.items[0].longitude)
    }
  }, [props]);

    return (
      <div>
        <Map center={[firstLat, firstLong]} zoom={11}>
          <TileLayer
            attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          
             { props.items && props.items.map((mark,id) => (
              <Marker 
                key={id}
                icon={ mapIcon }
                position={[
                  mark.latitude, 
                  mark.longitude
                ]}
                onClick= {() =>{
                  setActiveItem(mark)
                }}
              />
            ))};

            {activeItem && (
              <Popup 
                position={[
                  activeItem.latitude, 
                  activeItem.longitude
                ]}
                onClose={() =>{
                  setActiveItem(null);
                }}
              >
              <div>
                <h2>{activeItem.title}</h2>
              <a target="_blanc" href={props.details + activeItem["offer"]["offerID"]+'&type='+activeItem["offer"]["offerTypeId"]}>Détails</a>
              </div>
              </Popup>
            )}
        </Map>
        </div>
    )
}

export default FamilyMap;