import React from 'react';
import './game.css';
import astroImage from '../images/image.png';
import Footer from './footer';

var words = {
  'homem': true,
  'brasil' : false,
  'astronauta' : true,
  'terra': false
}

function GameWindow() {
  return (
    
    <div className="Game">
      
      <header className="Game-header w-full mt-12">
        <div className='columns-2 w-full flex items-center justify-between'>

          <div className='pl-20'>
            <div className='timer rounded-full'><p className='timerText'>30</p></div>
          </div>

          <div className='items-center content-center'>
            <h1 className="logo font-bold">WHY.C</h1>
          </div>

          <div className='pr-20'>
            <div className='timer rounded-full'><p className='timerText'>1/5</p></div>
          </div>
        </div>

        <div className='pt-8'>
          <img src={astroImage} alt='astro' className='genImg'/>
        </div>
        
      </header>
      <div className="divMain">
        <InputGuess/>
        <HistoryGuess/>
      </div>

      <Footer/>
    </div>
  );
}

function InputGuess() {
  return (
    <div className="inputWord pt-10">
        <input
          type="text"
          name="inputGuess"
          id="inputGuess"
          className="block w-full rounded-md py-1.5 pr-20 sm:text-sm sm:leading-6 inputLabel"
          placeholder="Digite uma palavra"
        />
    </div>
  )
}

function HistoryGuess() {
  return (
    <div className='pt-20'>
      {Object.entries(words).map(([word, isTrue]) => (
        <div className='pt-2'>
        <div key={word} className={`rectangle ${isTrue ? 'colorRight' : 'colorWrong'} `}>
          <p className={`text-center text-guess ${isTrue ? "text-accept" : "text-wrong"}`}>{word}</p>
        </div>
        </div>
      ))}
    </div>
  )
}

export default GameWindow;