import React, { createContext, useContext, useReducer, useCallback } from 'react';

const UndoRedoContext = createContext();

const initialState = {
  past: [],
  present: null,
  future: []
};

const reducer = (state, action) => {
  switch (action.type) {
    case 'UNDO':
      if (state.past.length === 0) return state;
      const previous = state.past[state.past.length - 1];
      const newPast = state.past.slice(0, -1);
      return {
        past: newPast,
        present: previous,
        future: [state.present, ...state.future]
      };
    case 'REDO':
      if (state.future.length === 0) return state;
      const next = state.future[0];
      const newFuture = state.future.slice(1);
      return {
        past: [...state.past, state.present],
        present: next,
        future: newFuture
      };
    case 'SET':
      return {
        past: [...state.past, state.present],
        present: action.payload,
        future: []
      };
    default:
      return state;
  }
};

export const UndoRedoProvider = ({ children }) => {
  const [state, dispatch] = useReducer(reducer, initialState);

  const undo = useCallback(() => {
    dispatch({ type: 'UNDO' });
  }, []);

  const redo = useCallback(() => {
    dispatch({ type: 'REDO' });
  }, []);

  const setState = useCallback((newState) => {
    dispatch({ type: 'SET', payload: newState });
  }, []);

  return (
    <UndoRedoContext.Provider value={{ state, undo, redo, setState }}>
      {children}
    </UndoRedoContext.Provider>
  );
};

export const useUndoRedo = () => {
  const context = useContext(UndoRedoContext);
  if (!context) {
    throw new Error('useUndoRedo must be used within an UndoRedoProvider');
  }
  return context;
}; 