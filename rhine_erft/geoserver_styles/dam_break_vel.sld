<?xml version="1.0" encoding="UTF-8"?>
<StyledLayerDescriptor version="1.0.0" 
    xmlns="http://www.opengis.net/sld" 
    xmlns:ogc="http://www.opengis.net/ogc" 
    xmlns:xlink="http://www.w3.org/1999/xlink" 
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
    xsi:schemaLocation="http://www.opengis.net/sld StyledLayerDescriptor.xsd">
  <NamedLayer>
    <Name>red_ramp_1_5_steps_0_to_15</Name>
    <UserStyle>
      <Title>Red Ramp (1.5 Steps, 0 to 15)</Title>
      <Abstract>A red colormap transition with 1.5 intervals for values between 0 and 15, where 0 is fully transparent.</Abstract>
      <FeatureTypeStyle>
        <Rule>
          <RasterSymbolizer>
            <ColorMap type="ramp">
              <!-- Value 0m: Fully Transparent -->
              <ColorMapEntry color="#FFFFFF" quantity="0" opacity="0.0" label="0 m/s (Transparent)"/>
              
              <!-- 1.5m Step Intervals (>0m to 15m) -->
              <ColorMapEntry color="#FF7373" quantity="0.01" opacity="1.0" label="> 0 m/s"/>
              <ColorMapEntry color="#FF4D4D" quantity="1.5" opacity="1.0" label="1.5 m/s"/>
              <ColorMapEntry color="#FF2626" quantity="3.0" opacity="1.0" label="3.0 m/s"/>
              <ColorMapEntry color="#E60000" quantity="4.5" opacity="1.0" label="4.5 m/s"/>
              <ColorMapEntry color="#CC0000" quantity="6.0" opacity="1.0" label="6.0 m/s"/>
              <ColorMapEntry color="#B3000C" quantity="7.5" opacity="1.0" label="7.5 m/s"/>
              <ColorMapEntry color="#99000D" quantity="9.0" opacity="1.0" label="9.0 m/s"/>
              <ColorMapEntry color="#80000B" quantity="10.5" opacity="1.0" label="10.5 m/s"/>
              <ColorMapEntry color="#660008" quantity="12.0" opacity="1.0" label="12.0 m/s"/>
              <ColorMapEntry color="#4D0005" quantity="13.5" opacity="1.0" label="13.5 m/s"/>
              <ColorMapEntry color="#330003" quantity="15.0" opacity="1.0" label="15.0 m/s"/>
            </ColorMap>
          </RasterSymbolizer>
        </Rule>
      </FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>

