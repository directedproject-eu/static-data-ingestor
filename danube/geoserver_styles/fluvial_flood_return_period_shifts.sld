<?xml version="1.0" encoding="ISO-8859-1"?>
<StyledLayerDescriptor version="1.0.0" 
                       xsi:schemaLocation="http://www.opengis.net/sld StyledLayerDescriptor.xsd" 
                       xmlns="http://www.opengis.net/sld" 
                       xmlns:ogc="http://www.opengis.net/ogc" 
                       xmlns:xlink="http://www.w3.org/1999/xlink" 
                       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <NamedLayer>
    <Name>Return period shifts</Name>
    <UserStyle>
      <Title>Return period shifts</Title>
      <FeatureTypeStyle>
        <Rule>
          <Title>0 - 10</Title>
          <ogc:Filter>
            <ogc:And>
              <ogc:Or>
                <ogc:PropertyIsGreaterThanOrEqualTo>
                  <ogc:PropertyName>return_period</ogc:PropertyName>
                  <ogc:Literal>0</ogc:Literal>
                </ogc:PropertyIsGreaterThanOrEqualTo>
                <ogc:PropertyIsNull>
                  <ogc:PropertyName>return_period</ogc:PropertyName>
                </ogc:PropertyIsNull>
              </ogc:Or>
              <ogc:Or>
                <ogc:PropertyIsLessThan>
                  <ogc:PropertyName>return_period</ogc:PropertyName>
                  <ogc:Literal>10</ogc:Literal>
                </ogc:PropertyIsLessThan>
                <ogc:PropertyIsNull>
                  <ogc:PropertyName>return_period</ogc:PropertyName>
                </ogc:PropertyIsNull>
              </ogc:Or>
            </ogc:And>
          </ogc:Filter>
          <LineSymbolizer>
            <Stroke>
              <CssParameter name="Stroke">#81e7ff</CssParameter>
              <CssParameter name="stroke-width">3</CssParameter>
            </Stroke>
          </LineSymbolizer>
        </Rule>
        <Rule>
          <Title>10 - 20</Title>
          <ogc:Filter>
            <ogc:And>
              <ogc:PropertyIsGreaterThanOrEqualTo>
                <ogc:PropertyName>return_period</ogc:PropertyName>
                <ogc:Literal>10</ogc:Literal>
              </ogc:PropertyIsGreaterThanOrEqualTo>
              <ogc:PropertyIsLessThan>
                <ogc:PropertyName>return_period</ogc:PropertyName>
                <ogc:Literal>20</ogc:Literal>
              </ogc:PropertyIsLessThan>
            </ogc:And>
          </ogc:Filter>
          <LineSymbolizer>
            <Stroke>
              <CssParameter name="Stroke">#71bae4</CssParameter>
              <CssParameter name="stroke-width">3</CssParameter>
            </Stroke>
          </LineSymbolizer>
        </Rule>
        <Rule>
          <Title>20 - 30</Title>
          <ogc:Filter>
            <ogc:And>
              <ogc:PropertyIsGreaterThanOrEqualTo>
                <ogc:PropertyName>return_period</ogc:PropertyName>
                <ogc:Literal>20</ogc:Literal>
              </ogc:PropertyIsGreaterThanOrEqualTo>
              <ogc:PropertyIsLessThan>
                <ogc:PropertyName>return_period</ogc:PropertyName>
                <ogc:Literal>30</ogc:Literal>
              </ogc:PropertyIsLessThan>
            </ogc:And>
          </ogc:Filter>
          <LineSymbolizer>
            <Stroke>
              <CssParameter name="Stroke">#6291c9</CssParameter>
              <CssParameter name="stroke-width">3</CssParameter>
            </Stroke>
          </LineSymbolizer>
        </Rule>
        <Rule>
          <Title>30 - 40</Title>
          <ogc:Filter>
            <ogc:And>
              <ogc:PropertyIsGreaterThanOrEqualTo>
                <ogc:PropertyName>return_period</ogc:PropertyName>
                <ogc:Literal>30</ogc:Literal>
              </ogc:PropertyIsGreaterThanOrEqualTo>
              <ogc:PropertyIsLessThan>
                <ogc:PropertyName>return_period</ogc:PropertyName>
                <ogc:Literal>40</ogc:Literal>
              </ogc:PropertyIsLessThan>
            </ogc:And>
          </ogc:Filter>
          <LineSymbolizer>
            <Stroke>
              <CssParameter name="Stroke">#546dab</CssParameter>
              <CssParameter name="stroke-width">3</CssParameter>
            </Stroke>
          </LineSymbolizer>
        </Rule>
        <Rule>
          <Title>40 - 50</Title>
          <ogc:Filter>
            <ogc:And>
              <ogc:PropertyIsGreaterThanOrEqualTo>
                <ogc:PropertyName>return_period</ogc:PropertyName>
                <ogc:Literal>40</ogc:Literal>
              </ogc:PropertyIsGreaterThanOrEqualTo>
              <ogc:PropertyIsLessThan>
                <ogc:PropertyName>return_period</ogc:PropertyName>
                <ogc:Literal>50</ogc:Literal>
              </ogc:PropertyIsLessThan>
            </ogc:And>
          </ogc:Filter>
          <LineSymbolizer>
            <Stroke>
              <CssParameter name="Stroke">#4c4a85</CssParameter>
              <CssParameter name="stroke-width">3</CssParameter>
            </Stroke>
          </LineSymbolizer>
        </Rule>
        <Rule>
          <Title>50 - 75</Title>
          <ogc:Filter>
            <ogc:And>
              <ogc:PropertyIsGreaterThanOrEqualTo>
                <ogc:PropertyName>return_period</ogc:PropertyName>
                <ogc:Literal>50</ogc:Literal>
              </ogc:PropertyIsGreaterThanOrEqualTo>
              <ogc:PropertyIsLessThan>
                <ogc:PropertyName>return_period</ogc:PropertyName>
                <ogc:Literal>75</ogc:Literal>
              </ogc:PropertyIsLessThan>
            </ogc:And>
          </ogc:Filter>
          <LineSymbolizer>
            <Stroke>
              <CssParameter name="Stroke">#502f59</CssParameter>
              <CssParameter name="stroke-width">3</CssParameter>
            </Stroke>
          </LineSymbolizer>
        </Rule>
        <Rule>
          <Title>75 - 100</Title>
          <ogc:Filter>
            <ogc:And>
              <ogc:PropertyIsGreaterThanOrEqualTo>
                <ogc:PropertyName>return_period</ogc:PropertyName>
                <ogc:Literal>75</ogc:Literal>
              </ogc:PropertyIsGreaterThanOrEqualTo>
              <ogc:PropertyIsLessThan>
                <ogc:PropertyName>return_period</ogc:PropertyName>
                <ogc:Literal>100</ogc:Literal>
              </ogc:PropertyIsLessThan>
            </ogc:And>
          </ogc:Filter>
          <LineSymbolizer>
            <Stroke>
              <CssParameter name="Stroke">#632a3e</CssParameter>
              <CssParameter name="stroke-width">3</CssParameter>
            </Stroke>
          </LineSymbolizer>
        </Rule>
        <Rule>
          <Title>100 - 125</Title>
          <ogc:Filter>
            <ogc:And>
              <ogc:PropertyIsGreaterThanOrEqualTo>
                <ogc:PropertyName>return_period</ogc:PropertyName>
                <ogc:Literal>100</ogc:Literal>
              </ogc:PropertyIsGreaterThanOrEqualTo>
              <ogc:PropertyIsLessThan>
                <ogc:PropertyName>return_period</ogc:PropertyName>
                <ogc:Literal>125</ogc:Literal>
              </ogc:PropertyIsLessThan>
            </ogc:And>
          </ogc:Filter>
          <LineSymbolizer>
            <Stroke>
              <CssParameter name="Stroke">#863c39</CssParameter>
              <CssParameter name="stroke-width">3</CssParameter>
            </Stroke>
          </LineSymbolizer>
        </Rule>
        <Rule>
          <Title>125 - 150</Title>
          <ogc:Filter>
            <ogc:And>
              <ogc:PropertyIsGreaterThanOrEqualTo>
                <ogc:PropertyName>return_period</ogc:PropertyName>
                <ogc:Literal>125</ogc:Literal>
              </ogc:PropertyIsGreaterThanOrEqualTo>
              <ogc:PropertyIsLessThan>
                <ogc:PropertyName>return_period</ogc:PropertyName>
                <ogc:Literal>150</ogc:Literal>
              </ogc:PropertyIsLessThan>
            </ogc:And>
          </ogc:Filter>
          <LineSymbolizer>
            <Stroke>
              <CssParameter name="Stroke">#a95a40</CssParameter>
              <CssParameter name="stroke-width">3</CssParameter>
            </Stroke>
          </LineSymbolizer>
        </Rule>
        <Rule>
          <Title>150 - 250</Title>
          <ogc:Filter>
            <ogc:And>
              <ogc:PropertyIsGreaterThanOrEqualTo>
                <ogc:PropertyName>return_period</ogc:PropertyName>
                <ogc:Literal>150</ogc:Literal>
              </ogc:PropertyIsGreaterThanOrEqualTo>
              <ogc:PropertyIsLessThan>
                <ogc:PropertyName>return_period</ogc:PropertyName>
                <ogc:Literal>250</ogc:Literal>
              </ogc:PropertyIsLessThan>
            </ogc:And>
          </ogc:Filter>
          <LineSymbolizer>
            <Stroke>
              <CssParameter name="Stroke">#c77c4b</CssParameter>
              <CssParameter name="stroke-width">3</CssParameter>
            </Stroke>
          </LineSymbolizer>
        </Rule>
        <Rule>
          <Title>250 - 500</Title>
          <ogc:Filter>
            <ogc:And>
              <ogc:PropertyIsGreaterThanOrEqualTo>
                <ogc:PropertyName>return_period</ogc:PropertyName>
                <ogc:Literal>250</ogc:Literal>
              </ogc:PropertyIsGreaterThanOrEqualTo>
              <ogc:PropertyIsLessThan>
                <ogc:PropertyName>return_period</ogc:PropertyName>
                <ogc:Literal>500</ogc:Literal>
              </ogc:PropertyIsLessThan>
            </ogc:And>
          </ogc:Filter>
          <LineSymbolizer>
            <Stroke>
              <CssParameter name="Stroke">#e3a358</CssParameter>
              <CssParameter name="stroke-width">3</CssParameter>
            </Stroke>
          </LineSymbolizer>
        </Rule>
        <Rule>
          <Title> > 500</Title>
          <ogc:Filter>
            <ogc:And>
              <ogc:PropertyIsGreaterThanOrEqualTo>
                <ogc:PropertyName>return_period</ogc:PropertyName>
                <ogc:Literal>500</ogc:Literal>
              </ogc:PropertyIsGreaterThanOrEqualTo>
              <ogc:PropertyIsLessThan>
                <ogc:PropertyName>return_period</ogc:PropertyName>
                <ogc:Literal>1000000</ogc:Literal>
              </ogc:PropertyIsLessThan>
            </ogc:And>
          </ogc:Filter>
          <LineSymbolizer>
            <Stroke>
              <CssParameter name="Stroke">#ffcf67</CssParameter>
              <CssParameter name="stroke-width">3</CssParameter>
            </Stroke>
          </LineSymbolizer>
        </Rule>
      </FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>