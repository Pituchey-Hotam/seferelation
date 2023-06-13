import React, { Component } from 'react';
import axios from 'axios';
import { Form, Input, Button, List, Typography } from 'antd';

const { Item } = List;

class ApiList extends Component {
  constructor(props) {
    super(props);
    this.state = {
      userInput: { sefaria_link: '' },
      relations: [],
      searchTerm: ''
    };
  }

  componentDidMount() {
    this.fetchRelations();
  }

  componentDidUpdate(prevProps, prevState) {
    if (prevState.searchTerm !== this.state.searchTerm) {
      this.fetchRelations();
    }
  }

  fetchRelations = () => {
    axios.get(`/api/relations?sefaria_link=${this.state.searchTerm}`)
      .then(response => {
        this.setState({ relations: response.data.relations || [] });
      });
  }

  handleSearchChange = event => {
    this.setState({
      userInput: { sefaria_link: event.target.value }
    });
  }

  handleSearchSubmit = event => {
    this.setState({ searchTerm: this.state.userInput.sefaria_link });
  }

  render() {
    const { userInput, relations } = this.state;

    return (
      <div>
        <Typography.Title level={2}>חיפוש מקורות לימוד</Typography.Title>
        <Typography.Paragraph>
          Search relations with seferelation api (by @ykaner):
          <br />
          בשביל לחפש העתיקו קישור מספריא לדבר שאותו אתם לומדים, לדוגמא:
          <br />
          https://www.sefaria.org.il/Genesis.1.1
        </Typography.Paragraph>

        <Form onFinish={this.handleSearchSubmit}>
          <Form.Item>
            <Input value={userInput.sefaria_link} onChange={this.handleSearchChange} />
          </Form.Item>
          <Form.Item>
            <Button type="primary" htmlType="submit">Search</Button>
          </Form.Item>
        </Form>

        <List
          header={<Typography.Title level={3}>Results</Typography.Title>}
          dataSource={relations}
          renderItem={item => (
            <Item id={item[1]}>
              <Typography.Text mark><a href={item[0]}>{item[1]}</a></Typography.Text> {item[0]}
            </Item>
          )}
        />
      </div>
    );
  }
}

export default ApiList;
