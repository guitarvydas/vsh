#!/bin/bash
swipl -g 'use_module(library(http/json))' -g 'consult(fb).' -g 'consult(component).' 'consult(names).' -g 'consult(code).' -g 'consult(jsoncomponent).'
      
