<StyledLayerDescriptor xmlns="http://www.opengis.net/sld"
                       xmlns:ogc="http://www.opengis.net/ogc"
                       xmlns:xlink="http://www.w3.org/1999/xlink"
                       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.opengis.net/sld
                                                                                                 http://schemas.opengis.net/sld/1.0.0/StyledLayerDescriptor.xsd" version="1.0.0">
  <NamedLayer>
    <Name>lidar_elevation</Name>
    <UserStyle>
      <FeatureTypeStyle>
        <Title>lidar_elevation</Title>
        <Rule>
          <RasterSymbolizer>
            <ColorMap extended = 'true' type='ramp'>
              <ColorMapEntry color = '#440154' quantity = '-10' label='-10'/>
              <ColorMapEntry color = '#482878' quantity = '30' label='30'/>
              <ColorMapEntry color = '#3e4989' quantity = '60' label='60'/>
              <ColorMapEntry color = '#31688e' quantity = '90' label='90'/>
              <ColorMapEntry color = '#26828e' quantity = '120' label='120'/>
              <ColorMapEntry color = '#1f9e89' quantity = '150' label='150'/>
              <ColorMapEntry color = '#35b779' quantity = '180' label='180'/>
              <ColorMapEntry color = '#6ece58' quantity = '210' label='210'/>
              <ColorMapEntry color = '#b5de2b' quantity = '240' label='240'/>
              <ColorMapEntry color = '#fde725' quantity = '270' label='270'/>
            </ColorMap>
          </RasterSymbolizer>
        </Rule>
      </FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>
