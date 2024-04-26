<script lang="ts">
  	import { Block, BlockTitle } from "@gradio/atoms";
    import { createEventDispatcher } from "svelte";

    export let label: string;
    export let show_label: boolean = true;
    export let info: string | undefined = undefined;
    export let min = 0;
    export let max = 100;
    export let selected_min = 25;
    export let selected_max = 75;

    const dispatch = createEventDispatcher();

    function handle_change(selected_min, selected_max): void {
      dispatch("change", [selected_min, selected_max]);
    }
  
    function handle_min_change(event) {
      selected_min = parseInt(event.target.value);
      if (selected_min > selected_max) {
        selected_max = selected_min;
      }
    }
  
    function handle_max_change(event) {
      selected_max = parseInt(event.target.value);
      if (selected_max < selected_min) {
        selected_min = selected_max;
      }
    }

    $: handle_change(selected_min, selected_max);

    $: rangeLine = `
      left: ${( (selected_min - min) / (max - min)) * 100}%;
      width: ${ ((selected_max - selected_min) / (max - min)) * 100}%;
    `;

  </script>
  
  <Block container={true}>
    <div class="wrap">
      <div class="head">
          <BlockTitle {show_label} {info}>{label}</BlockTitle>
          <div class="numbers">
            <input
                aria-label={`max input for ${label}`}
                data-testid="max-input"
                type="number"
                bind:value={selected_max}
                min={min}
                max={max}
                disabled={false}
            />
            <input
              aria-label={`min input for ${label}`}
              data-testid="min-input"
              type="number"
              bind:value={selected_min}
              min={min}
              max={max}
              disabled={false}
            />
          </div>
      </div>
    </div>
    <div class="range-slider">
      <div class="range-bg"></div>
      <div class="range-line" style={rangeLine}></div>
      <input type="range" min={min} max={max} bind:value={selected_min} on:input={handle_min_change} />
      <input type="range" min={min} max={max} bind:value={selected_max} on:input={handle_max_change} />
    </div>
  </Block>


  
  <style>
    .wrap {
      display: flex;
      flex-direction: column;
      width: 100%;
	  }
    
    .head {
      display: flex;
      justify-content: space-between;
    }

    .numbers {
	  	display: flex;
      flex-direction: row-reverse;
      max-width: var(--size-6);
	  }

    input[type="number"] {
        display: block;
        position: relative;
        outline: none !important;
        box-shadow: var(--input-shadow);
        border: var(--input-border-width) solid var(--input-border-color);
        border-radius: var(--input-radius);
        background: var(--input-background-fill);
        padding: var(--size-2) var(--size-2);
        height: var(--size-6);
        color: var(--body-text-color);
        font-size: var(--input-text-size);
        line-height: var(--line-sm);
        text-align: center;
	}

    .range-slider {
      position: relative;
      width: 100%;
      height: 30px;
    }
  
    .range-slider input[type="range"] {
      position: absolute;
      left: 0;
      bottom: 0;
      width: 100%;
      appearance: none;
      outline: none;
      background: transparent;
      pointer-events: none;
    }
  
    .range-slider input[type="range"]::-webkit-slider-thumb {
      appearance: none;
      width: 20px;
      height: 20px;
      background: white;
      border-radius: 50%;
      border: solid 0.5px #ddd;
      pointer-events: auto;
      cursor: pointer;
    }
  
    .range-slider input[type="range"]::-moz-range-thumb {
      width: 20px;
      height: 20px;
      background: white;
      border-radius: 50%;
      border: solid 0.5px #ddd;
      pointer-events: auto;
      cursor: pointer;
    }
  
    .range-line {
      position: absolute;
      left: 0;
      bottom: 8px;
      height: 4px;
      background: var(--slider-color);
      pointer-events: none;
    }

    .range-bg {
      position: absolute;
      left: 0;
      width: 100%;
      bottom: 8px;
      height: 4px;
      z-index: 0;
      background: var(--neutral-200);
      pointer-events: none;
    }
  
  </style>