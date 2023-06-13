import React, { Component } from 'react';
import axios from 'axios';
import { Form, Input, Button, Table, Typography } from 'antd';
import { SearchOutlined } from '@ant-design/icons';

const { Column } = Table;

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
    event.preventDefault();
  }

  handleSearchMore = link => {
    this.setState({ userInput: { sefaria_link: link } });
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

        <Table
          dataSource={relations}
          rowKey={item => item[1]}
        >
          <Column title="Score" dataIndex={0} key={0} />
          <Column title="Link" dataIndex={1} key={1} />
          <Column
            title="Search More"
            key="searchMore"
            render={(text, record) => (
              <Button icon={<SearchOutlined />} onClick={() => this.handleSearchMore(record[1])} />
            )}
          />
        </Table>
      </div>
    );
  }
}

export default ApiList;
