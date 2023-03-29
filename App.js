/* 
Author: Ehsan Sabery Ghomy 
Date: April 8, 2022
File Name: App.js
Description: BlackJack Game Using React Native.
*/


import { Image,  Button,  StyleSheet, Text, View } from 'react-native';
import {useEffect, useState} from 'react'; 

let gameCards = {};
let botValues = [];
let userValues = [];


export default function App() {

  const cards = {
    backCard : "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Bicyclebackside.jpg/573px-Bicyclebackside.jpg?20100523173912",
    card:
    [
    {name: "C_10", value: 10, imageURL: "https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/English_pattern_10_of_clubs.svg/540px-English_pattern_10_of_clubs.svg.png?20170224203638"},
    {name: "D_10", value: 10, imageURL: "https://upload.wikimedia.org/wikipedia/commons/thumb/d/da/English_pattern_10_of_diamonds.svg/540px-English_pattern_10_of_diamonds.svg.png?20170224203639"},
    {name: "H_10", value: 10, imageURL: "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bb/English_pattern_10_of_hearts.svg/540px-English_pattern_10_of_hearts.svg.png?20170224203640"},
    {name: "S_10", value: 10, imageURL: "https://upload.wikimedia.org/wikipedia/commons/thumb/d/da/English_pattern_10_of_spades.svg/540px-English_pattern_10_of_spades.svg.png?20170224203642"},

    {name: "C_2", value: 2, imageURL: "https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/English_pattern_2_of_clubs.svg/540px-English_pattern_2_of_clubs.svg.png?20170224201513"},
    {name: "D_2", value: 2, imageURL: "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/Atlas_deck_2_of_diamonds.svg/540px-Atlas_deck_2_of_diamonds.svg.png?20140724040009"},
    {name: "H_2", value: 2, imageURL: "https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/English_pattern_2_of_hearts.svg/540px-English_pattern_2_of_hearts.svg.png?20170224201513"},
    {name: "S_2", value: 2, imageURL: "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0b/English_pattern_2_of_spades.svg/540px-English_pattern_2_of_spades.svg.png?20170224201514"},

    {name: "C_3", value: 3, imageURL: "https://upload.wikimedia.org/wikipedia/commons/thumb/1/14/English_pattern_3_of_clubs.svg/540px-English_pattern_3_of_clubs.svg.png?20170224203611"},
    {name: "D_3", value: 3, imageURL: "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2c/English_pattern_3_of_diamonds.svg/540px-English_pattern_3_of_diamonds.svg.png?20170224203612"},
    {name: "H_3", value: 3, imageURL: "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0f/English_pattern_3_of_hearts.svg/540px-English_pattern_3_of_hearts.svg.png?20170224203612"},
    {name: "S_3", value: 3, imageURL: "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/English_pattern_3_of_spades.svg/540px-English_pattern_3_of_spades.svg.png?20170224203616"},

    {name: "C_4", value: 4, imageURL: "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c0/English_pattern_4_of_clubs.svg/540px-English_pattern_4_of_clubs.svg.png?20170224203615"},
    {name: "D_4", value: 4, imageURL: "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/English_pattern_4_of_diamonds.svg/540px-English_pattern_4_of_diamonds.svg.png?20170224203616"},
    {name: "H_4", value: 4, imageURL: "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bb/English_pattern_4_of_hearts.svg/540px-English_pattern_4_of_hearts.svg.png?20170224203618"},
    {name: "S_4", value: 4, imageURL: "https://upload.wikimedia.org/wikipedia/commons/thumb/3/34/English_pattern_4_of_spades.svg/540px-English_pattern_4_of_spades.svg.png?20170224203618"},

    {name: "C_5", value: 5, imageURL: "https://upload.wikimedia.org/wikipedia/commons/thumb/7/74/English_pattern_5_of_clubs.svg/540px-English_pattern_5_of_clubs.svg.png?20170224203619"},
    {name: "D_5", value: 5, imageURL: "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/English_pattern_5_of_diamonds.svg/540px-English_pattern_5_of_diamonds.svg.png?20170224203621"},
    {name: "H_5", value: 5, imageURL: "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c6/English_pattern_5_of_hearts.svg/540px-English_pattern_5_of_hearts.svg.png?20170224203621"},
    {name: "S_5", value: 5, imageURL: "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9c/English_pattern_5_of_spades.svg/540px-English_pattern_5_of_spades.svg.png?20170224203622"},

    {name: "C_6", value: 6, imageURL: "https://upload.wikimedia.org/wikipedia/commons/thumb/0/02/English_pattern_6_of_clubs.svg/540px-English_pattern_6_of_clubs.svg.png?20170224203624"},
    {name: "D_6", value: 6, imageURL: "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/English_pattern_6_of_diamonds.svg/540px-English_pattern_6_of_diamonds.svg.png?20170224203624"},
    {name: "H_6", value: 6, imageURL: "https://upload.wikimedia.org/wikipedia/commons/thumb/d/da/English_pattern_6_of_hearts.svg/540px-English_pattern_6_of_hearts.svg.png?20170224203624"},
    {name: "S_6", value: 6, imageURL: "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/English_pattern_6_of_spades.svg/540px-English_pattern_6_of_spades.svg.png?20170224203626"},

    {name: "C_7", value: 7, imageURL: "https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/English_pattern_7_of_clubs.svg/540px-English_pattern_7_of_clubs.svg.png?20170224203626"},
    {name: "D_7", value: 7, imageURL: "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5d/English_pattern_7_of_diamonds.svg/540px-English_pattern_7_of_diamonds.svg.png?20170224203627"},
    {name: "H_7", value: 7, imageURL: "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cb/English_pattern_7_of_hearts.svg/540px-English_pattern_7_of_hearts.svg.png?20170224203630"},
    {name: "S_7", value: 7, imageURL: "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/English_pattern_7_of_spades.svg/540px-English_pattern_7_of_spades.svg.png?20170224203630"},

    {name: "C_8", value: 8, imageURL: "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f0/English_pattern_8_of_clubs.svg/540px-English_pattern_8_of_clubs.svg.png?20170224203630"},
    {name: "D_8", value: 8, imageURL: "https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/English_pattern_8_of_diamonds.svg/540px-English_pattern_8_of_diamonds.svg.png?20170224203633"},
    {name: "H_8", value: 8, imageURL: "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/English_pattern_8_of_hearts.svg/540px-English_pattern_8_of_hearts.svg.png?20170224203633"},
    {name: "S_8", value: 8, imageURL: "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/English_pattern_8_of_spades.svg/540px-English_pattern_8_of_spades.svg.png?20170224203633"},

    {name: "C_9", value: 9, imageURL: "https://upload.wikimedia.org/wikipedia/commons/thumb/1/14/English_pattern_9_of_clubs.svg/540px-English_pattern_9_of_clubs.svg.png?20170224203635"},
    {name: "D_9", value: 9, imageURL: "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f5/English_pattern_9_of_diamonds.svg/540px-English_pattern_9_of_diamonds.svg.png?20170224203636"},
    {name: "H_9", value: 9, imageURL: "https://upload.wikimedia.org/wikipedia/commons/thumb/2/22/English_pattern_9_of_hearts.svg/540px-English_pattern_9_of_hearts.svg.png?20170224203635"},
    {name: "S_9", value: 9, imageURL: "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f0/English_pattern_9_of_spades.svg/540px-English_pattern_9_of_spades.svg.png?20170224203639"},

    {name: "C_A", value: 11, imageURL: "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/English_pattern_ace_of_clubs.svg/540px-English_pattern_ace_of_clubs.svg.png?20170224203642"},
    {name: "D_A", value: 11, imageURL: "https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/English_pattern_ace_of_diamonds.svg/540px-English_pattern_ace_of_diamonds.svg.png?20170224203643"},
    {name: "H_A", value: 11, imageURL: "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/English_pattern_ace_of_hearts.svg/540px-English_pattern_ace_of_hearts.svg.png?20170224203646"},
    {name: "S_A", value: 11, imageURL: "https://upload.wikimedia.org/wikipedia/commons/thumb/1/19/English_pattern_ace_of_spades.svg/540px-English_pattern_ace_of_spades.svg.png?20170224203646"},

    {name: "C_J", value: 10, imageURL: "https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/English_pattern_jack_of_clubs.svg/540px-English_pattern_jack_of_clubs.svg.png?20170224203646"},
    {name: "D_J", value: 10, imageURL: "https://upload.wikimedia.org/wikipedia/commons/thumb/1/16/English_pattern_jack_of_diamonds.svg/540px-English_pattern_jack_of_diamonds.svg.png?20170224203648"},
    {name: "H_J", value: 10, imageURL: "https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/English_pattern_jack_of_hearts.svg/540px-English_pattern_jack_of_hearts.svg.png?20170224203649"},
    {name: "S_J", value: 10, imageURL: "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/English_pattern_jack_of_spades.svg/540px-English_pattern_jack_of_spades.svg.png?20170224203648"},

    {name: "C_K", value: 10, imageURL: "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/English_pattern_king_of_clubs.svg/540px-English_pattern_king_of_clubs.svg.png?20170224203651"},
    {name: "D_K", value: 10, imageURL: "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1c/English_pattern_king_of_diamonds.svg/540px-English_pattern_king_of_diamonds.svg.png?20170224203651"},
    {name: "H_K", value: 10, imageURL: "https://upload.wikimedia.org/wikipedia/commons/thumb/1/14/English_pattern_king_of_hearts.svg/540px-English_pattern_king_of_hearts.svg.png?20170224203652"},
    {name: "S_K", value: 10, imageURL: "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/English_pattern_king_of_spades.svg/540px-English_pattern_king_of_spades.svg.png?20170224203656"},

    {name: "C_Q", value: 10, imageURL: "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b3/English_pattern_queen_of_clubs.svg/540px-English_pattern_queen_of_clubs.svg.png?20170224203656"},
    {name: "D_Q", value: 10, imageURL: "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/English_pattern_queen_of_diamonds.svg/540px-English_pattern_queen_of_diamonds.svg.png?20170224203656"},
    {name: "H_Q", value: 10, imageURL: "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9d/English_pattern_queen_of_hearts.svg/540px-English_pattern_queen_of_hearts.svg.png?20170224203659"},
    {name: "S_Q", value: 10, imageURL: "https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/English_pattern_queen_of_spades.svg/540px-English_pattern_queen_of_spades.svg.png?20170224203659"}            
    ]
  };

  const [botImg1, setBotImg1] = useState({display:"flex", imageVal: cards.backCard});
  const [botImg2, setBotImg2] = useState({display:"flex", imageVal: cards.backCard});
  const [botImg3, setBotImg3] = useState({display:"flex", imageVal: cards.backCard});
  const [botImg4, setBotImg4] = useState({display:"flex", imageVal: cards.backCard});
  const [botImg5, setBotImg5] = useState({display:"flex", imageVal: cards.backCard});

  const [userImg1, setUserImg1] = useState({display:"flex", imageVal: cards.backCard});
  const [userImg2, setUserImg2] = useState({display:"flex", imageVal: cards.backCard});
  const [userImg3, setUserImg3] = useState({display:"flex", imageVal: cards.backCard});
  const [userImg4, setUserImg4] = useState({display:"flex", imageVal: cards.backCard});
  const [userImg5, setUserImg5] = useState({display:"flex", imageVal: cards.backCard});

  const [hitDisabled, setHitDisabled] = useState(true);
  const [stayDisabled, setStayDisabled] = useState(true);

  
 
  

  const initFunction = async function()
  {
    setHitDisabled(true);
    setStayDisabled(true);
    gameCards = {};
    botValues = [];
    userValues = [];
    setBotImg1({display:"flex", imageVal: cards.backCard});
    setBotImg2({display:"flex", imageVal: cards.backCard});
    setBotImg3({display:"flex", imageVal: cards.backCard});
    setBotImg4({display:"flex", imageVal: cards.backCard});
    setBotImg5({display:"flex", imageVal: cards.backCard});

    setUserImg1({display:"flex", imageVal: cards.backCard});
    setUserImg2({display:"flex", imageVal: cards.backCard});
    setUserImg3({display:"flex", imageVal: cards.backCard});
    setUserImg4({display:"flex", imageVal: cards.backCard});
    setUserImg5({display:"flex", imageVal: cards.backCard});

  }

  const handleHit = async function()
  { 
    let isA;
    let random;
    let userSum;

    if (userValues.length == 2)
    {
      //userVal3
      random = Math.floor(Math.random() * gameCards.card.length); 
      if (gameCards.card[random].value == 11)
          isA=1;
      else 
          isA= 0;

      userValues.push({ value: gameCards.card[random].value , image: gameCards.card[random].imageURL, ace: isA} );
      gameCards.card = gameCards.card.filter(x => x.name != gameCards.card[random].name);

      setUserImg3({display:"flex", imageVal: userValues[2].image});

      userSum = userValues[0].value + userValues[1].value + userValues[2].value;
      
      if (userSum > 21){
           if (userValues[0].ace == 1){
              userSum = userSum - 10;
              userValues[0].value = 1;
              userValues[0].ace = 0;
             
              if (userSum > 21){
                //lost
                setHitDisabled(true);
                setStayDisabled(true);
                await new Promise(r => setTimeout(r,1000));
                alert("You Lost!");
                
              }
              else {
                setHitDisabled(false);
                setStayDisabled(false);
              }
           }
           else if (userValues[1].ace == 1){
             userSum = userSum - 10;
             userValues[1].value = 1;
             userValues[1].ace = 0;
             if (userSum > 21){
              //lost
              setHitDisabled(true);
              setStayDisabled(true);
              await new Promise(r => setTimeout(r,1000));
              alert("You Lost!");
             }
             else {
              setHitDisabled(false);
              setStayDisabled(false);
             }
             
           }
           else if (userValues[2].ace == 1){
            userSum = userSum - 10;
            userValues[2].value = 1;
            userValues[2].ace = 0;
            if (userSum > 21){
              //lost
              setHitDisabled(true);
              setStayDisabled(true);
              await new Promise(r => setTimeout(r,1000));
              alert("You Lost!");
            }
            else {
              setHitDisabled(false);
              setStayDisabled(false);
            }
           }
           else {
            //lost
            setHitDisabled(true);
            setStayDisabled(true);
            await new Promise(r => setTimeout(r,1000));
            alert("You Lost!");
           }

      }
      else {
        setHitDisabled(false);
        setStayDisabled(false);
      }

    }
    else if (userValues.length == 3)
    {
      
        
       //userVal4
       random = Math.floor(Math.random() * gameCards.card.length); 
       if (gameCards.card[random].value == 11)
           isA=1;
       else 
           isA= 0;
 
       userValues.push({ value: gameCards.card[random].value , image: gameCards.card[random].imageURL, ace: isA} );
       gameCards.card = gameCards.card.filter(x => x.name != gameCards.card[random].name);
 
       setUserImg4({display:"flex", imageVal: userValues[3].image});
 
       userSum = userValues[0].value + userValues[1].value + userValues[2].value + userValues[3].value;
       
       if (userSum > 21){
            if (userValues[0].ace == 1){
               userSum = userSum - 10;
               userValues[0].value = 1;
               userValues[0].ace = 0;
               if (userSum > 21){
                //lost
                setHitDisabled(true);
                setStayDisabled(true);
                await new Promise(r => setTimeout(r,1000));
                alert("You Lost!");
               }
               else {
                setHitDisabled(false);
                setStayDisabled(false);
               }
            }
            else if (userValues[1].ace == 1){
              userSum = userSum - 10;
              userValues[1].value = 1;
              userValues[1].ace = 0;
              if (userSum > 21){
                //lost
                setHitDisabled(true);
                setStayDisabled(true);
                await new Promise(r => setTimeout(r,1000));
                alert("You Lost!");
              }
              else {
                setHitDisabled(false);
                setStayDisabled(false);
              }
              
            }
            else if (userValues[2].ace == 1){
             userSum = userSum - 10;
             userValues[2].value = 1;
             userValues[2].ace = 0;
             if (userSum > 21){
              //lost
              setHitDisabled(true);
              setStayDisabled(true);
              await new Promise(r => setTimeout(r,1000));
              alert("You Lost!");
             }
             else {
              setHitDisabled(false);
              setStayDisabled(false);
             }
            }
            else if (userValues[3].ace == 1){
              userSum = userSum - 10;
              userValues[3].value = 1;
              userValues[3].ace = 0;
              if (userSum > 21){
                //lost
                setHitDisabled(true);
                setStayDisabled(true);
                await new Promise(r => setTimeout(r,1000));
                alert("You Lost!");
              }
              else {
                setHitDisabled(false);
                setStayDisabled(false);
              }
            }
            else {
             //lost
             setHitDisabled(true);
             setStayDisabled(true);
             await new Promise(r => setTimeout(r,1000));
             alert("You Lost!");
            }
 
       }
       else {
         setHitDisabled(false);
         setStayDisabled(false);
       }
     

    }
    else if (userValues.length == 4)
    {

      
        //userVal5
        random = Math.floor(Math.random() * gameCards.card.length); 
        if (gameCards.card[random].value == 11)
            isA=1;
        else 
            isA= 0;
  
        userValues.push({ value: gameCards.card[random].value , image: gameCards.card[random].imageURL, ace: isA} );
        gameCards.card = gameCards.card.filter(x => x.name != gameCards.card[random].name);
  
        setUserImg5({display:"flex", imageVal: userValues[4].image});
  
        userSum = userValues[0].value + userValues[1].value + userValues[2].value + userValues[3].value + userValues[4].value;
        
        if (userSum > 21){
             if (userValues[0].ace == 1){
                userSum = userSum - 10;
                userValues[0].value = 1;
                userValues[0].ace = 0;
                if (userSum > 21){
                 //lost
                 setHitDisabled(true);
                 setStayDisabled(true);
                 await new Promise(r => setTimeout(r,1000));
                 alert("You Lost!");
                }
                else {
                 setHitDisabled(true);
                 setStayDisabled(true);
                 await new Promise(r => setTimeout(r,1000));
                 alert("You Won!");
                }
             }
             else if (userValues[1].ace == 1){
               userSum = userSum - 10;
               userValues[1].value = 1;
               userValues[1].ace = 0;
               if (userSum > 21){
                 //lost
                 setHitDisabled(true);
                 setStayDisabled(true);
                 await new Promise(r => setTimeout(r,1000));
                 alert("You Lost!");
               }
               else {
                setHitDisabled(true);
                setStayDisabled(true);
                await new Promise(r => setTimeout(r,1000));
                alert("You Won!");
               }
               
             }
             else if (userValues[2].ace == 1){
              userSum = userSum - 10;
              userValues[2].value = 1;
              userValues[2].ace = 0;
              if (userSum > 21){
               //lost
               setHitDisabled(true);
               setStayDisabled(true);
               await new Promise(r => setTimeout(r,1000));
               alert("You Lost!");
              }
              else {
                setHitDisabled(true);
                setStayDisabled(true);
                await new Promise(r => setTimeout(r,1000));
                alert("You Won!");
              }
             }
             else if (userValues[3].ace == 1){
               userSum = userSum - 10;
               userValues[3].value = 1;
               userValues[3].ace = 0;
               if (userSum > 21){
                 //lost
                 setHitDisabled(true);
                 setStayDisabled(true);
                 await new Promise(r => setTimeout(r,1000));
                 alert("You Lost!");
               }
               else {
                setHitDisabled(true);
                setStayDisabled(true);
                await new Promise(r => setTimeout(r,1000));
                alert("You Won!");
               }
             }
             else if (userValues[4].ace == 1){
              userSum = userSum - 10;
              userValues[4].value = 1;
              userValues[4].ace = 0;
              if (userSum > 21){
                //lost
                setHitDisabled(true);
                setStayDisabled(true);
                await new Promise(r => setTimeout(r,1000));
                alert("You Lost!");
              }
              else {
               setHitDisabled(true);
               setStayDisabled(true);
               await new Promise(r => setTimeout(r,1000));
               alert("You Won!");
              }
             }
             else {
              //lost
              setHitDisabled(true);
              setStayDisabled(true);
              await new Promise(r => setTimeout(r,1000));
              alert("You Lost!");
             }
  
        }
        else {
               setHitDisabled(true);
               setStayDisabled(true);
               await new Promise(r => setTimeout(r,1000));
               alert("You Won!");
        }
    
    }
  }

  const handleStay = async function()
  {
    setHitDisabled(true);
    setStayDisabled(true);
    let flagContinue = false;
    let usersum=0;
    let random;
    let isA=0;
    for (let i=0; i< userValues.length; i++){
      usersum += userValues[i].value;
    }
    
    let botsum = 0;
    for (let i=0; i< botValues.length; i++){
      botsum += botValues[i].value;
    }

    await new Promise(r => setTimeout(r,750));

    setBotImg2({display:"flex", imageVal: botValues[1].image});

    //first check bot
    if (botsum >21){

      if (botValues[0].ace == 1){
        botsum = botsum - 10;
        botValues[0].value = 1;
        botValues[0].ace = 0;
        if (botsum > 21){
          //bot lost
          await new Promise(r => setTimeout(r,1000));
          alert("You Won!");
          flagContinue = false;
        }
        else {
          flagContinue= true;
          
        }
      
      }
      else if (botValues[1].ace == 1){
        
        botsum = botsum - 10;
        botValues[1].value = 1;
        botValues[1].ace = 0;
        if (botsum > 21){
          //bot lost
          await new Promise(r => setTimeout(r,1000));
          alert("You Won!");
          flagContinue = false;
        }
        else {
          flagContinue= true;
          
        }
        
      }
      else {
           //bot lost
           await new Promise(r => setTimeout(r,1000));
           alert("You Won!");
           flagContinue = false;

      }
    }
    else if (botsum >= 17){
       flagContinue= false;
       if (usersum > botsum){
        await new Promise(r => setTimeout(r,1000));
        alert("You Won!");
       }
       else if (usersum < botsum){
        await new Promise(r => setTimeout(r,1000));
        alert("You Lost!");
       }
       else {
        await new Promise(r => setTimeout(r,1000));
        alert("Tie!");
       }


    }
    else {
       flagContinue= true;
    }


    //double-check if bot is >=17 when bot has 2 cards.
    if (flagContinue)
    {
      if (botsum >= 17){
        flagContinue = false;
        if (usersum > botsum){
          await new Promise(r => setTimeout(r,1000));
          alert("You Won!");
         }
         else if (usersum < botsum){
          await new Promise(r => setTimeout(r,1000));
          alert("You Lost!");
         }
         else {
          await new Promise(r => setTimeout(r,1000));
          alert("Tie!");
         }

      }

    }


    //bot will draw card 3:
    if (flagContinue){
          
      random = Math.floor(Math.random() * gameCards.card.length ); 
      if (gameCards.card[random].value == 11)
          isA=1;
      else 
          isA= 0;
      
      botValues.push({ value: gameCards.card[random].value , image: gameCards.card[random].imageURL, ace: isA} );
      gameCards.card = gameCards.card.filter(x => x.name != gameCards.card[random].name);
      

      await new Promise(r => setTimeout(r,750));

      setBotImg3({display:"flex", imageVal: botValues[2].image});
      
      botsum += botValues[2].value;

      if (botsum >21){

        if (botValues[0].ace == 1){
          botsum = botsum - 10;
          botValues[0].value = 1;
          botValues[0].ace = 0;
          if (botsum > 21){
            //bot lost
            await new Promise(r => setTimeout(r,1000));
            alert("You Won!");
            flagContinue = false;
          }
          else {
            flagContinue= true;
            
          }
        
        }
        else if (botValues[1].ace == 1){
          
          botsum = botsum - 10;
          botValues[1].value = 1;
          botValues[1].ace = 0;
          if (botsum > 21){
            //bot lost
            await new Promise(r => setTimeout(r,1000));
            alert("You Won!");
            flagContinue = false;
          }
          else {
            flagContinue= true;
            
          }
          
        }
        else if (botValues[2].ace == 1){
          
          botsum = botsum - 10;
          botValues[2].value = 1;
          botValues[2].ace = 0;
          if (botsum > 21){
            //bot lost
            await new Promise(r => setTimeout(r,1000));
            alert("You Won!");
            flagContinue = false;
          }
          else {
            flagContinue= true;
            
          }
          
        }

        else {
             //bot lost
             await new Promise(r => setTimeout(r,1000));
             alert("You Won!");
             flagContinue = false;
  
        }
      }
      else if (botsum >= 17){
         flagContinue= false;
         if (usersum > botsum){
          await new Promise(r => setTimeout(r,1000));
          alert("You Won!");
         }
         else if (usersum < botsum){
          await new Promise(r => setTimeout(r,1000));
          alert("You Lost!");
         }
         else {
          await new Promise(r => setTimeout(r,1000));
          alert("Tie!");
         }
  
  
      }
      else {
         flagContinue= true;
      }
     
       
    } //end of bot will draw card 3.

    //double-check if bot is >=17 when bot has 3 cards.
    if (flagContinue)
    {
      if (botsum >= 17){
        flagContinue = false;
        if (usersum > botsum){
          await new Promise(r => setTimeout(r,1000));
          alert("You Won!");
        }
        else if (usersum < botsum){
          await new Promise(r => setTimeout(r,1000));
          alert("You Lost!");
        }
        else {
          await new Promise(r => setTimeout(r,1000));
          alert("Tie!");
        }

      }

    }


    //bot will draw card 4:
    if (flagContinue){
          
      random = Math.floor(Math.random() * gameCards.card.length ); 
      if (gameCards.card[random].value == 11)
          isA=1;
      else 
          isA= 0;
      
      botValues.push({ value: gameCards.card[random].value , image: gameCards.card[random].imageURL, ace: isA} );
      gameCards.card = gameCards.card.filter(x => x.name != gameCards.card[random].name);
      

      await new Promise(r => setTimeout(r,750));

      setBotImg4({display:"flex", imageVal: botValues[3].image});
      
      botsum += botValues[3].value;

      if (botsum >21){

        if (botValues[0].ace == 1){
          botsum = botsum - 10;
          botValues[0].value = 1;
          botValues[0].ace = 0;
          if (botsum > 21){
            //bot lost
            await new Promise(r => setTimeout(r,1000));
            alert("You Won!");
            flagContinue = false;
          }
          else {
            flagContinue= true;
            
          }
        
        }
        else if (botValues[1].ace == 1){
          
          botsum = botsum - 10;
          botValues[1].value = 1;
          botValues[1].ace = 0;
          if (botsum > 21){
            //bot lost
            await new Promise(r => setTimeout(r,1000));
            alert("You Won!");
            flagContinue = false;
          }
          else {
            flagContinue= true;
            
          }
          
        }
        else if (botValues[2].ace == 1){
          
          botsum = botsum - 10;
          botValues[2].value = 1;
          botValues[2].ace = 0;
          if (botsum > 21){
            //bot lost
            await new Promise(r => setTimeout(r,1000));
            alert("You Won!");
            flagContinue = false;
          }
          else {
            flagContinue= true;
            
          }
          
        }
        else if (botValues[3].ace == 1){
          
          botsum = botsum - 10;
          botValues[3].value = 1;
          botValues[3].ace = 0;
          if (botsum > 21){
            //bot lost
            await new Promise(r => setTimeout(r,1000));
            alert("You Won!");
            flagContinue = false;
          }
          else {
            flagContinue= true;
            
          }
          
        }

        else {
             //bot lost
             await new Promise(r => setTimeout(r,1000));
             alert("You Won!");
             flagContinue = false;
  
        }
      }
      else if (botsum >= 17){
         flagContinue= false;
         if (usersum > botsum){
          await new Promise(r => setTimeout(r,1000));
          alert("You Won!");
         }
         else if (usersum < botsum){
          await new Promise(r => setTimeout(r,1000));
          alert("You Lost!");
         }
         else {
          await new Promise(r => setTimeout(r,1000));
          alert("Tie!");
         }
  
  
      }
      else {
         flagContinue= true;
      }
      
    } //end of bot will draw card 4.

     //double-check if bot is >=17 when bot has 4 cards.
     if (flagContinue)
     {
       if (botsum >= 17){
         flagContinue = false;
         if (usersum > botsum){
           await new Promise(r => setTimeout(r,1000));
           alert("You Won!");
         }
         else if (usersum < botsum){
           await new Promise(r => setTimeout(r,1000));
           alert("You Lost!");
         }
         else {
           await new Promise(r => setTimeout(r,1000));
           alert("Tie!");
         }
 
       }
 
     }


    //bot will draw card 5:  if sum value for bot for 5 cards is less than 22, bot automatically wins.     
    if (flagContinue){
          
      random = Math.floor(Math.random() * gameCards.card.length ); 
      if (gameCards.card[random].value == 11)
          isA=1;
      else 
          isA= 0;
      
      botValues.push({ value: gameCards.card[random].value , image: gameCards.card[random].imageURL, ace: isA} );
      gameCards.card = gameCards.card.filter(x => x.name != gameCards.card[random].name);
      

      await new Promise(r => setTimeout(r,750));

      setBotImg5({display:"flex", imageVal: botValues[4].image});
      
      botsum += botValues[4].value;

      if (botsum >21){

        if (botValues[0].ace == 1){
          botsum = botsum - 10;
          botValues[0].value = 1;
          botValues[0].ace = 0;
          if (botsum > 21){
            //bot lost
            await new Promise(r => setTimeout(r,1000));
            alert("You Won!");
            flagContinue = false;
          }
          else {
            flagContinue= true;
            
          }
        
        }
        else if (botValues[1].ace == 1){
          
          botsum = botsum - 10;
          botValues[1].value = 1;
          botValues[1].ace = 0;
          if (botsum > 21){
            //bot lost
            await new Promise(r => setTimeout(r,1000));
            alert("You Won!");
            flagContinue = false;
          }
          else {
            flagContinue= true;
            
          }
          
        }
        else if (botValues[2].ace == 1){
          
          botsum = botsum - 10;
          botValues[2].value = 1;
          botValues[2].ace = 0;
          if (botsum > 21){
            //bot lost
            await new Promise(r => setTimeout(r,1000));
            alert("You Won!");
            flagContinue = false;
          }
          else {
            flagContinue= true;
            
          }
          
        }
        else if (botValues[3].ace == 1){
          
          botsum = botsum - 10;
          botValues[3].value = 1;
          botValues[3].ace = 0;
          if (botsum > 21){
            //bot lost
            await new Promise(r => setTimeout(r,1000));
            alert("You Won!");
            flagContinue = false;
          }
          else {
            flagContinue= true;
            
          }
          
        }
        else if (botValues[4].ace == 1){
          
          botsum = botsum - 10;
          botValues[4].value = 1;
          botValues[4].ace = 0;
          if (botsum > 21){
            //bot lost
            await new Promise(r => setTimeout(r,1000));
            alert("You Won!");
            flagContinue = false;
          }
          else {
            flagContinue= true;
            
          }
          
        }

        else {
             //bot lost
             await new Promise(r => setTimeout(r,1000));
             alert("You Won!");
             flagContinue = false;
  
        }
      }
      else {  //bot with 5 cards is less than 22, bot wins.
         flagContinue= false;
         await new Promise(r => setTimeout(r,1000));
         alert("You Lost!");
  
      }
     
      
    } //end of bot will draw card 5.


    //double-check if bot is < 22 when bot has 5 cards. if flagContinue is true, bot wins.
    if (flagContinue)
    {
      await new Promise(r => setTimeout(r,1000));
      alert("You Lost!");
    }

  }


  
  const handleNewGame = async function()
  {
    gameCards = cards;
    botValues = [];
    userValues = [];
    let isA = 0;

    //botVal1
    let random = Math.floor(Math.random() * gameCards.card.length ); 
    if (gameCards.card[random].value == 11)
        isA=1;
    else 
        isA= 0;
    
    botValues.push({ value: gameCards.card[random].value , image: gameCards.card[random].imageURL, ace: isA} );
    gameCards.card = gameCards.card.filter(x => x.name != gameCards.card[random].name);
    
    //botVal2
    random = Math.floor(Math.random() * gameCards.card.length);
    if (gameCards.card[random].value == 11)
        isA=1;
    else 
        isA= 0;

    botValues.push({ value: gameCards.card[random].value , image: gameCards.card[random].imageURL, ace: isA} );
    gameCards.card = gameCards.card.filter(x => x.name != gameCards.card[random].name);

    //userVal1
    random = Math.floor(Math.random() * gameCards.card.length); 
    if (gameCards.card[random].value == 11)
        isA=1;
    else 
        isA= 0;

    userValues.push({ value: gameCards.card[random].value , image: gameCards.card[random].imageURL, ace:isA} );
    gameCards.card = gameCards.card.filter(x => x.name != gameCards.card[random].name);

    //userVal2
    random = Math.floor(Math.random() * gameCards.card.length); 
    if (gameCards.card[random].value == 11)
        isA=1;
    else 
        isA= 0;

    userValues.push({ value: gameCards.card[random].value , image: gameCards.card[random].imageURL, ace:isA} );
    gameCards.card = gameCards.card.filter(x => x.name != gameCards.card[random].name);


   
    
    setBotImg1({display:"flex", imageVal: cards.backCard});
    setBotImg2({display:"flex", imageVal: cards.backCard});
    setBotImg3({display:"none", imageVal: cards.backCard});
    setBotImg4({display:"none", imageVal: cards.backCard});
    setBotImg5({display:"none", imageVal: cards.backCard});


    setUserImg1({display:"flex", imageVal: cards.backCard});
    setUserImg2({display:"flex", imageVal: cards.backCard});
    setUserImg3({display:"none", imageVal: cards.backCard});
    setUserImg4({display:"none", imageVal: cards.backCard});
    setUserImg5({display:"none", imageVal: cards.backCard});
    await new Promise(r => setTimeout(r,750));
    setUserImg1({display:"flex", imageVal: userValues[0].image});
    await new Promise(r => setTimeout(r,750));

    setBotImg1({display:"flex", imageVal: botValues[0].image});
    await new Promise(r => setTimeout(r,750));

    setUserImg2({display:"flex", imageVal: userValues[1].image});
    await new Promise(r => setTimeout(r,750));

    setBotImg2({display:"flex", imageVal: cards.backCard});
   
    

  

    //checking to see if user is 21: instant Win:
    let userSum = userValues[0].value + userValues[1].value;

    if (userSum > 21){
        //game starts, but you need to reduce 1 ace with value=11 to value=1

        userValues[0].value = 1;
        userValues[0].ace = 0;
        setHitDisabled(false);
        setStayDisabled(false);
     

    }
    else if (userSum == 21) {
       //Winner
       setHitDisabled(true);
       setStayDisabled(true);
       await new Promise(r => setTimeout(r,1000));
       alert("You Won!");
    }
    else {
      //game starts
      setHitDisabled(false);
      setStayDisabled(false);
    }
    
  }


  const handleJoke = async function()
  {
    let response = await fetch("http://api.icndb.com/jokes/random?limitTo=[nerdy]");
    let json = await response.json();
    alert(json.value.joke);
  }



  useEffect(
    initFunction,
    []
  )



  return (
   
         <View style={styles.container}>
           
            
            <Text style= { {fontSize: 18, color: 'white', textAlign: "center" }}>{"\n\n\n\n"}Computer{"\n"}</Text>
            
            <View style={{flexDirection: "row"}}>
              <View style={{flex:1}}>
                <Image source={{uri: botImg1.imageVal}} 
                    style={{width:90, height:90, resizeMode: 'contain', display: botImg1.display}} />
              </View>
              <View style={{flex:1}}>
                <Image source={{uri: botImg2.imageVal}} 
                    style={{width:90, height:90, resizeMode: 'contain', display: botImg2.display}} />
              </View>
              <View style={{flex:1}}>
                <Image source={{uri: botImg3.imageVal}} 
                    style={{width:90, height:90, resizeMode: 'contain', display: botImg3.display}} />
              </View>
              <View style={{flex:1}}>
                <Image source={{uri: botImg4.imageVal}} 
                    style={{width:90, height:90, resizeMode: 'contain', display: botImg4.display}} />  
              </View>
              <View style={{flex:1}}>
                <Image source={{uri: botImg5.imageVal}} 
                    style={{width:90, height:90, resizeMode: 'contain', display: botImg5.display}} />
              </View>
            </View>




            <Text style= { {fontSize: 18, color: 'white', textAlign: "center" }}>{"\n\n\n\n\n\n\n"}You{"\n"}</Text>
            
            <View style={{flexDirection: "row"}}>
              <View style={{flex:1}}>
                 <Image source={{uri: userImg1.imageVal}} 
                    style={{width:90, height:90, resizeMode: 'contain', display: userImg1.display}} />
              </View>
              <View style={{flex:1}}>
                <Image source={{uri: userImg2.imageVal}} 
                    style={{width:90, height:90, resizeMode: 'contain', display: userImg2.display}} />
              </View>
              <View style={{flex:1}}>
                <Image source={{uri: userImg3.imageVal}} 
                    style={{width:90, height:90, resizeMode: 'contain', display: userImg3.display}} />
              </View>
              <View style={{flex:1}}>
                <Image source={{uri: userImg4.imageVal}} 
                    style={{width:90, height:90, resizeMode: 'contain', display: userImg4.display}} />
              </View>
              <View style={{flex:1}}>
                <Image source={{uri: userImg5.imageVal}} 
                    style={{width:90, height:90, resizeMode: 'contain', display: userImg5.display}} />
              </View>
            </View>

            <Text>{"\n\n"}</Text>


            <View style={{flexDirection: "row"}}>
                  <View style={{flex:4}}>
                      <Button onPress={ () => handleHit()}
                              title= "HIT"
                              color= "blue" 
                              disabled= {hitDisabled} /> 
                  </View>
                  <View style={{flex:4}}>
                      <Button onPress={ () =>  handleStay()}
                              title= "STAY"
                              color= "red"
                              disabled= {stayDisabled} />
                  </View>

                  <View style={{flex:3}}>
                      <Button onPress={ () => handleNewGame()}
                              title= "NEW GAME"
                              color= "gray"/>
                  </View>


            </View>

            <Text>{"\n\n"}</Text>
            <View style={{flexDirection: "row"}}>
                   <View style={{flex:1}}>
                      <Button onPress={ () => handleJoke()}
                              title= "GET A CHUCK NORRIS NERDY JOKE"
                              color= "gray"/>
                  </View>
            </View>




          </View>

  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: 'green'
  }
});
