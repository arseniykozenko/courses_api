import { Button, Result } from 'antd';

const NotFoundPage = () => {
  return (
    <Result
      status="404"
      title="404"
      subTitle="Извините, страница не найдена"
      extra={
        <Button type="primary" href="/">
          Вернуться на главную
        </Button>
      }
    />
  );
};

export default NotFoundPage;